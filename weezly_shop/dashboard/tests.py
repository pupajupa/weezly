from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Product, Category
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, EditProductForm
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class DashboardViewsTest(TestCase):

    def setUp(self):
        self.image_file = self.get_temporary_image(tempfile.NamedTemporaryFile(suffix='.png').name)

        self.manager = User.objects.create_user(
            email='manager@example.com',
            full_name='Manager User',
            password='password123'
        )
        self.manager.is_manager = True
        self.manager.save()

        self.regular_user = User.objects.create_user(
            email='user@example.com',
            full_name='Regular User',
            password='password123'
        )

        self.category = Category.objects.create(title='Electronics')

        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            price=100,
            category=self.category,
            description='Test Description'
        )
        self.product.image.save('test.png', SimpleUploadedFile(
            name='test.png',
            content=open(self.image_file, 'rb').read(),
            content_type='image/png'
        ))
        self.product.save()

        self.order = Order.objects.create(user=self.regular_user, paid=False)
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=100,
            quantity=2
        )

    def get_temporary_image(self, temp_file):
        image = Image.new('RGB', (100, 100))
        image.save(temp_file, 'png')
        return temp_file

    def login_manager(self):
        self.client.login(email='manager@example.com', password='password123')

    def test_access_denied_for_non_manager(self):
        self.client.login(email='user@example.com', password='password123')
        response = self.client.get(reverse('dashboard:products'))
        self.assertEqual(response.status_code, 404)

    def test_products_view(self):
        self.login_manager()
        response = self.client.get(reverse('dashboard:products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')
        self.assertIn('products', response.context)
        self.assertIn('categories', response.context)

    def test_products_filter_by_category(self):
        self.login_manager()
        url = reverse('dashboard:products') + f'?category={self.category.id}'
        response = self.client.get(url)
        products = list(response.context['products'])
        self.assertTrue(all(p.category == self.category for p in products))

    def test_products_sorting(self):
        self.login_manager()
        sort_params = {
            'newest': '-date_created',
            'oldest': 'date_created',
            'price_high': '-price',
            'price_low': 'price',
            'name_asc': 'title',
            'name_desc': '-title'
        }

        for param, field in sort_params.items():
            with self.subTest(param=param):
                url = reverse('dashboard:products') + f'?sort={param}'
                response = self.client.get(url)
                products = list(response.context['products'].order_by(field))
                response_products = list(response.context['products'])
                self.assertEqual(products, response_products)

    def test_add_product_get(self):
        self.login_manager()
        response = self.client.get(reverse('dashboard:add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddProductForm)

    def test_add_product_post_valid(self):
        self.login_manager()
        form_data = {
            'title': 'New Product',
            'slug': 'new-product',
            'price': 50,
            'description': 'Great product!',
            'category': self.category.id
        }
        image = open(self.image_file, 'rb').read()
        uploaded = SimpleUploadedFile(name='test.jpg', content=image, content_type='image/jpeg')

        form_data['image'] = uploaded
        response = self.client.post(reverse('dashboard:add_product'), data=form_data, follow=True)
        self.assertRedirects(response, reverse('dashboard:add_product'))
        self.assertTrue(Product.objects.filter(title='New Product').exists())

    def test_delete_product(self):
        self.login_manager()
        product_id = self.product.id
        response = self.client.get(reverse('dashboard:delete_product', args=[product_id]))
        self.assertRedirects(response, reverse('dashboard:products'))
        with self.assertRaises(Product.DoesNotExist):
            self.product.refresh_from_db()

    def test_edit_product_get(self):
        self.login_manager()
        response = self.client.get(reverse('dashboard:edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditProductForm)

    def test_edit_product_post_valid(self):
        self.login_manager()
        form_data = {
            'title': 'Updated Product',
            'slug': 'updated-product',
            'price': 120,
            'description': 'Updated Description',
            'category': self.category.id
        }
        image = open(self.image_file, 'rb').read()
        uploaded = SimpleUploadedFile(name='test.jpg', content=image, content_type='image/jpeg')
        form_data['image'] = uploaded

        response = self.client.post(
            reverse('dashboard:edit_product', args=[self.product.id]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('dashboard:products'))
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.title, 'Updated Product')

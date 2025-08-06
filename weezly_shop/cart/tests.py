from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product, Category
from decimal import Decimal
from PIL import Image
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()


class CartSessionTests(TestCase):

    def setUp(self):
        self.image_file = self.get_temporary_image(tempfile.NamedTemporaryFile(suffix='.png').name)

        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            full_name='Test User'
        )

        self.category = Category.objects.create(title='Electronics')

        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            price=Decimal('100.00'),
            category=self.category,
            description='Test Description'
        )
        self.product.image.save('test.png', SimpleUploadedFile(
            name='test.png',
            content=open(self.image_file, 'rb').read(),
            content_type='image/png'
        ))
        self.product.save()

    def get_temporary_image(self, temp_file):
        """Создаёт временное изображение"""
        image = Image.new('RGB', (100, 100))
        image.save(temp_file, 'png')
        return temp_file

    # === add_to_cart ===
    def test_add_to_cart_login_required(self):
        url = reverse('cart:add_to_cart', args=[self.product.id])
        response = self.client.get(url)
        expected_url = f'/accounts/login/'
        self.assertRedirects(response, expected_url)

    def test_add_to_cart_invalid_form(self):
        self.client.login(email='testuser@example.com', password='password123')
        url = reverse('cart:add_to_cart', args=[self.product.id])

        form_data = {'quantity': 'invalid'}
        response = self.client.post(url, data=form_data)
        session = self.client.session
        self.assertNotIn(str(self.product.id), session.get('cart', {}))

    # === show_cart ===
    def test_show_cart_login_required(self):
        url = reverse('cart:show_cart')
        response = self.client.get(url)
        expected_url = f'/accounts/login/'
        self.assertRedirects(response, expected_url)

    def test_show_cart_empty(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('cart:show_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_show_cart_with_items(self):
        self.client.login(email='testuser@example.com', password='password123')
        session = self.client.session

        # Добавляем товар вручную через сессию
        session['cart'] = {
            str(self.product.id): {
                'quantity': 2,
                'price': int(self.product.price),
                'title': self.product.title,
                'slug': self.product.slug,
                'image': self.product.image.name if self.product.image else ''
            }
        }
        session.save()

        response = self.client.get(reverse('cart:show_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_remove_from_cart(self):
        self.client.login(email='testuser@example.com', password='password123')
        session = self.client.session

        session['cart'] = {
            str(self.product.id): {
                'quantity': 2,
                'price': str(self.product.price),
                'title': self.product.title,
                'slug': self.product.slug,
                'image': self.product.image.name if self.product.image else ''
            }
        }
        session.save()

        url = reverse('cart:remove_from_cart', args=[self.product.id])
        response = self.client.get(url)
        session = self.client.session
        self.assertRedirects(response, reverse('cart:show_cart'))
        self.assertNotIn(str(self.product.id), session.get('cart', {}))

    def test_remove_from_cart_not_in_cart(self):
        self.client.login(email='testuser@example.com', password='password123')
        url = reverse('cart:remove_from_cart', args=[self.product.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('cart:show_cart'))

        session = self.client.session
        self.assertNotIn(str(self.product.id), session.get('cart', {}))
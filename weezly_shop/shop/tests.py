import tempfile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product, Category, PriceTracking
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile

def get_temporary_image(temp_file):
    image = Image.new('RGB', (100, 100))
    image.save(temp_file, 'png')
    return temp_file

User = get_user_model()

class ShopViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            full_name='Test User'
        )

        image_file = tempfile.NamedTemporaryFile(suffix='.png').name
        image = get_temporary_image(image_file)

        self.category = Category.objects.create(title='Electronics')

        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            price=Decimal('100.00'),
            category=self.category,
            description='Test Description',
            popularity=5
        )
        self.product.image.save('test.png', SimpleUploadedFile(
            name='test.png',
            content=open(image, 'rb').read(),
            content_type='image/png'
        ))
        self.product.save()

        self.tracking = PriceTracking.objects.create(
            user=self.user,
            product=self.product,
            desired_price=Decimal('90.00')
        )

    def test_home_page_view(self):
        response = self.client.get(reverse('shop:home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_page.html')
        self.assertIn('popular_products', response.context)
        self.assertIn('discounted_products', response.context)
        self.assertIn('categories', response.context)

    def test_shop_page_view(self):
        response = self.client.get(reverse('shop:shop_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_page.html')
        self.assertIn('products', response.context)

    def test_product_detail_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('shop:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertEqual(response.context['product'], self.product)

    def test_product_detail_adds_to_viewed(self):
        self.client.login(email='testuser@example.com', password='password123')
        session = self.client.session
        session['viewed_products'] = []
        session.save()
        response = self.client.get(reverse('shop:product_detail', args=[self.product.slug]))
        viewed = response.wsgi_request.session.get('viewed_products', [])
        self.assertIn(self.product.id, viewed)

    def test_product_detail_shows_tracking_status(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('shop:product_detail', args=[self.product.slug]))
        self.assertEqual(response.context['price_tracking'], self.tracking)

    def test_product_detail_adds_to_favorites(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(reverse('shop:product_detail', args=[self.product.slug]), {
            'desired_price': '90.00'
        })
        tracking = PriceTracking.objects.get(user=self.user, product=self.product)
        self.assertEqual(tracking.desired_price, Decimal('90.00'))

    # === favorites views ===
    def test_add_to_favorites(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('shop:add_to_favorites', args=[self.product.id]))
        self.assertRedirects(response, reverse('shop:product_detail', args=[self.product.slug]))
        self.assertIn(self.product, self.user.likes.all())

    def test_remove_from_favorites(self):
        self.client.login(email='testuser@example.com', password='password123')
        self.user.likes.add(self.product)
        response = self.client.get(reverse('shop:remove_from_favorites', args=[self.product.id]))
        self.assertRedirects(response, reverse('shop:product_detail', args=[self.product.slug]))
        self.assertNotIn(self.product, self.user.likes.all())

    def test_favorites_page(self):
        self.client.login(email='testuser@example.com', password='password123')
        self.user.likes.add(self.product)
        response = self.client.get(reverse('shop:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorites.html')
        self.assertIn(self.product, response.context['products'])
        self.assertIn(self.tracking, response.context['price_trackings'])

    def test_search_view(self):
        response = self.client.get(reverse('shop:search') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, response.context['products'])

    def test_cancel_price_tracking(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('shop:cancel_price_tracking', args=[self.product.id]))
        with self.assertRaises(PriceTracking.DoesNotExist):
            self.tracking.refresh_from_db()

    # === faq and about ===
    def test_faq_page(self):
        response = self.client.get(reverse('shop:faq_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')

    def test_about_page(self):
        response = self.client.get(reverse('shop:about_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
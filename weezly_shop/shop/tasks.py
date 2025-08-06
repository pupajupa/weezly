# shop/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from online_shop import settings
from .models import PriceTracking


def check_price_tracking_for_product(product_id):
    from .models import Product
    product = Product.objects.get(id=product_id)

    trackings = PriceTracking.objects.filter(product=product)

    for tracking in trackings:
        if product.price <= tracking.desired_price:
            context = {
                'user': tracking.user,
                'product': product,
                'new_price': product.price,
                'product_url': product.get_absolute_url()
            }
            print(f"Отправка уведомления на почту {tracking.user.email} по товару {product.title}")
            message = render_to_string('price_drop_notification.html', context)
            send_mail(
                subject='The price of the product has decreased!',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[tracking.user.email],
                html_message=message
            )

from django.core.mail import send_mail

from online_shop import settings
from django.template.loader import render_to_string

def send_price_drop_notification(user, product, new_price):
    subject = 'The price of the product has decreased!'
    
    # Контекст для email
    context = {
        'user': user,
        'product': product,
        'new_price': new_price,
        'product_url': product.get_absolute_url()  # Предположим, у вас есть метод для получения URL товара
    }

    # Генерация HTML-содержимого письма
    message = render_to_string('price_drop_notification.html', context)
    print(f"Отправка уведомления на почту {user.email} по товару {product.title}")
    # Отправка письма
    send_mail(
        subject,
        '',  # Текстовое содержание письма (если необходимо)
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,  # HTML-версия письма
    )
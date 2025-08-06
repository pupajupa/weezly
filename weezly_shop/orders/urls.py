from django.urls import path, include

from orders import views

app_name = "orders"

urlpatterns = [
    path('create', views.create_order, name='create_order'),
    path('list', views.user_orders, name='user_orders'),
    path('fake-payment/<int:order_id>', views.fake_payment, name='pay_order'),
    path('', include('paypal.standard.ipn.urls')),
    path('capture-paypal-order/', views.capture_paypal_order, name='capture_paypal_payment'),
    path('create-paypal-order/', views.create_paypal_order, name='create_paypal_order'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),  # ← добавить name
    path('payment-failed/<int:order_id>/', views.payment_failed, name='payment_failed'), 
    path('checkout/<int:order_id>', views.checkout, name='checkout'),
]
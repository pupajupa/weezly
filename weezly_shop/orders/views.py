import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone
import requests

from .models import Order, OrderItem
from cart.utils.cart import Cart

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
import uuid
from django.views.decorators.csrf import csrf_exempt



@login_required
def create_order(request):
    cart = Cart(request)
    order = Order.objects.create(
        user=request.user,
        order_number=str(uuid.uuid4())[:10]  # ← Добавлено
    )
    for item in cart:
        OrderItem.objects.create(
            order=order, product=item['product'],
            price=item['price'], quantity=item['quantity']
        )
    return redirect('orders:checkout', order_id=order.id)


@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'checkout.html', {'order': order})


@login_required
def fake_payment(request, order_id):
    cart = Cart(request)
    cart.clear()
    order = get_object_or_404(Order, id=order_id)
    order.status = True
    order.save()
    return redirect('orders:user_orders')


@login_required
def user_orders(request):
    orders = request.user.orders.all()
    context = {'title':'Orders', 'orders': orders}
    return render(request, 'user_orders.html', context)

def payment_success(request, order_id):
    cart = Cart(request)
    cart.clear()
    order = get_object_or_404(Order, id=order_id)
    order.status = True
    order.save()
    return render(request, 'payment_success.html', {'order': order})

def payment_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment_failed.html', {'order' : order})


def get_paypal_access_token():
    client_id = settings.PAYPAL_CLIENT_ID
    secret = settings.PAYPAL_SECRET

    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, data=data, auth=(client_id, secret), headers={"Accept": "application/json"})
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to get access token")

@csrf_exempt
def create_paypal_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total = float(data['total'].replace(',', '.'))
            currency = data.get('currency', 'USD')
            order_id = data.get('order_id')
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)

        access_token = get_paypal_access_token()
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(total),
                    }
                }
            ],
            "application_context": {
                "brand_name": "WEEZLY",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "PAY_NOW",
            },
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            return JsonResponse({"orderID": order_id})
        else:
            return JsonResponse({"error": "Failed to create order"}, status=400)
        
        
def capture_paypal_order(request, order_id):
    access_token = get_paypal_access_token()
    order_id_from_client = request.GET.get("orderID")
    
    if not order_id_from_client:
        return JsonResponse({"error": "Missing orderID"}, status=400)

    url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id_from_client}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(url, json={}, headers=headers)
    if response.status_code == 201:
        order = get_object_or_404(Order, id=order_id)
        order.paid = True
        order.save()

        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Capture failed", "status": response.status_code, "details": response.json()}, status=response.status_code)
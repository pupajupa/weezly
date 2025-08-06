from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests

from online_shop import settings
from .decorators import login_required_message
from cart.utils.cart import Cart
from .forms import QuantityForm
from shop.models import Product
from orders.models import Order

@login_required_message
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    product.popularity += 1
    product.save()
    form = QuantityForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'])
        messages.success(request, 'Added to your cart!', 'info')
    return redirect('shop:product_detail', slug=product.slug)


@login_required_message
def show_cart(request):
    cart = Cart(request)

    order = Order.objects.filter(user=request.user)  # или другой фильтр

    context = {
        'title': 'Cart',
        'cart': cart,
        'order': order  # ← это нужно!
    }
    return render(request, 'cart.html', context)



@login_required_message
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:show_cart')


        

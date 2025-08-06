from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.cache import cache
from .decorators import login_required_message
import random
from .utils import send_price_drop_notification
from django.db.models import F, Q
from shop.models import Product, Category
from cart.forms import QuantityForm

from celery import shared_task
from .models import PriceTracking


def check_price_tracking():
    price_trackings = PriceTracking.objects.filter(is_notified=False)
    for tracking in price_trackings:
        if tracking.product.price <= tracking.desired_price:
            tracking.is_notified = True
            tracking.save()
            send_price_drop_notification(tracking.user, tracking.product, tracking.product.price)

@login_required_message
def cancel_price_tracking(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        # Удаляем отслеживание этого продукта для текущего пользователя
        PriceTracking.objects.filter(user=request.user, product=product).delete()
    return redirect('shop:product_detail', slug=product.slug)

def paginat(request, list_objects):
	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj

def shop_page(request):
    sort = request.GET.get('sort', '')  # Сортировка из GET-параметра

    if sort == 'price_asc':
        products = Product.objects.order_by('price')
    elif sort == 'price_desc':
        products = Product.objects.order_by('-price')
    elif sort == 'newest':
        products = Product.objects.order_by('-date_created')  # Предполагается наличие поля created_at
    elif sort == 'popular':
        products = Product.objects.order_by('-popularity')  # Предполагается наличие поля popularity
    else:
        products = Product.objects.all()

    context = {'products': paginat(request, products)}
    return render(request, 'shop_page.html', context)

def home_page(request):
    # Популярные товары (по популярности)
    popular_products = Product.objects.filter(popularity__gt=0).order_by('-popularity')[:5]

    # Товары с понижением цены (используем PriceTracking)
    discounted_products = Product.objects.filter(
        pricetracking__desired_price__lt=F('price'),
        pricetracking__is_notified=False
    ).distinct()[:6]
    categories = Category.objects.exclude(slug__isnull=True).exclude(slug__exact='')
    # История просмотров – для персональных рекомендаций
    viewed = request.session.get('viewed_products', [])
    personal_recommendations = Product.objects.filter(id__in=viewed).order_by('?')[:5] if viewed else Product.objects.order_by('?')[:5]

    # Аксессуары к вашему заказу – пока что просто рандомные товары
    accessory_products = Product.objects.exclude(id__in=viewed).order_by('?')[:5]

    return render(request, 'home_page.html', {
        'popular_products': popular_products,
        'discounted_products': discounted_products,
        'personal_recommendations': personal_recommendations,
        'accessory_products': accessory_products,
        'categories': categories,
    })

def product_detail(request, slug):
    form = QuantityForm()
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]
    viewed = request.session.get('viewed_products', [])
    if product.id not in viewed:
        viewed.append(product.id)
        request.session['viewed_products'] = viewed[-20:]
    context = {
        'title': product.title,
        'product': product,
        'form': form,
        'favorites': 'favorites',
        'related_products': related_products
    }

    # Проверка, есть ли у пользователя этот товар в отслеживании
    tracking = None
    if request.user.is_authenticated:
        tracking = PriceTracking.objects.filter(user=request.user, product=product).first()
        context['price_tracking'] = tracking

    # Обработка формы отслеживания цены
    if request.method == 'POST' and 'desired_price' in request.POST:
        if not request.user.is_authenticated:
            messages.warning(request, "To track prices you need to log in to your account.")
            return redirect('login')  # или перенаправьте куда нужно

        desired_price = request.POST.get('desired_price')
        try:
            desired_price = float(desired_price)
            tracking, created = PriceTracking.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'desired_price': desired_price}
            )
            if not created:
                tracking.desired_price = desired_price
                tracking.save()
            check_price_tracking()
            messages.success(request, "You have subscribed to price drop notifications.")
        except ValueError:
            messages.error(request, "Incorrect price.")

        return redirect('shop:product_detail', slug= product.slug)

    # Избранное
    if request.user.is_authenticated and request.user.likes.filter(id=product.id).exists():
        context['favorites'] = 'remove'
    else:
        context['favorites'] = None

    return render(request, 'product_detail.html', context)


@login_required_message
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required_message
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:product_detail', slug=product.slug)

@login_required_message
def remove_from_favorites_shop_page(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:shop_page')

@login_required_message
def add_to_favorites_shop_page(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:shop_page')

@login_required_message
def remove_from_favorites_home_page(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:home_page')

@login_required_message
def add_to_favorites_home_page(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:home_page')


@login_required_message
def favorites(request):
    products = request.user.likes.all()
    price_trackings = PriceTracking.objects.filter(user=request.user)
    context = {
        'title': 'Favorites',
        'products': products,
        'price_trackings': price_trackings,  # Добавляем отслеживаемые товары
    }
    return render(request, 'favorites.html', context)


def search(request):
	query = request.GET.get('q')
	products = Product.objects.filter(title__icontains=query).all()
	context = {'products': paginat(request ,products)}
	return render(request, 'shop_page.html', context)


def filter_by_category(request, slug):
	"""when user clicks on parent category
	we want to show all products in its sub-categories too
	"""
	result = []
	category = Category.objects.filter(slug=slug).first()
	[result.append(product) \
		for product in Product.objects.filter(category=category.id).all()]
	# check if category is parent then get all sub-categories
	if not category.is_sub:
		sub_categories = category.sub_categories.all()
		# get all sub-categories products 
		for category in sub_categories:
			[result.append(product) \
				for product in Product.objects.filter(category=category).all()]
	context = {'products': paginat(request ,result)}
	return render(request, 'shop_page.html', context)

def faq_page(request):
    return render(request, 'faq.html')


def about_page(request):
    return render(request, 'about.html')
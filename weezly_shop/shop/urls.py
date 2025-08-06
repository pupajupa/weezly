from django.urls import path

from shop import views

app_name = "shop"

urlpatterns = [
	path('', views.home_page, name='home_page'),
    path('shop/',views.shop_page,name='shop_page'),
	path('<slug:slug>', views.product_detail, name='product_detail'),
	path('add/favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
	path('remove/favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('shop/add/favorites/<int:product_id>/', views.add_to_favorites_shop_page, name='add_to_favorites_shop_page'),
    path('shop/remove/favorites/<int:product_id>/', views.remove_from_favorites_shop_page, name='remove_from_favorites_shop_page'),
    path('home/add/favorites/<int:product_id>/', views.add_to_favorites_home_page, name='add_to_favorites_home_page'),
    path('home/remove/favorites/<int:product_id>/', views.remove_from_favorites_home_page, name='remove_from_favorites_home_page'),
	path('favorites/', views.favorites, name='favorites'),
	path('search/', views.search, name='search'),
	path('filter/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
    path('faqs/', views.faq_page, name='faq_page'),
    path('cancel-price-tracking/<int:product_id>/', views.cancel_price_tracking, name='cancel_price_tracking'),
    path('about-us/', views.about_page, name='about_page'),
]
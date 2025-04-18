from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/',
         views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove_cart_item/<int:product_id>/',
         views.remove_cart_item, name='remove_cart_item'),
]

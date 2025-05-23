from django.urls import path
from . import views
from . import payment

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<int:category_id>/',
         views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove_cart_item/<int:product_id>/',
         views.remove_cart_item, name='remove_cart_item'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('create-order/', views.create_order_from_cart, name='create_order'),

    # 綠界金流相關 URL - 簡化版
    path('ecpay-payment/<int:order_id>/',
         payment.EcpayPayment.create_order_payment, name='ecpay_payment'),
    path('ecpay-payment-return/',
         payment.ecpay_payment_return, name='ecpay_payment_return'),
]

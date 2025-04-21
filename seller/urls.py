from django.urls import path
from . import views

app_name = 'seller'  # 命名空間

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/',
         views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/',
         views.delete_product, name='delete_product'),
    path('orders/', views.order_list, name='order_list'),
]

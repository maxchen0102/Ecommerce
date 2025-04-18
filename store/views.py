from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category, Product, Cart, CartItem, Order, OrderItem
import uuid
from decimal import Decimal


def _cart_id(request):
    """Generate or get cart ID from session"""
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart


def home(request):
    """Home page view"""
    products = Product.objects.all().filter(available=True)
    context = {
        'products': products,
    }
    return render(request, 'store/home.html', context)


def product_list(request, category_id=None):
    """View to list all products or filter by category"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, product_id):
    """View to display a single product"""
    product = get_object_or_404(Product, id=product_id, available=True)
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)


def cart(request):
    """View to display cart"""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total = sum(item.product.price * item.quantity for item in cart_items)
        quantity = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        quantity = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    """Add a product to cart"""
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, product_id):
    """Remove a single instance of product from cart"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    """Remove entire cart item regardless of quantity"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect('cart')


def order_list(request):
    """View to display all orders"""
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_list.html', context)


def order_detail(request, order_id):
    """View to display an order"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)


def create_order_from_cart(request):
    """View to create an order from the cart items"""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items:
            return redirect('cart')

        # 計算總金額
        total = sum(item.product.price * item.quantity for item in cart_items)

        # 創建訂單
        order = Order.objects.create(
            total=Decimal(total),
            # 預設值，避免資料庫錯誤
            first_name="顧客",
            last_name="",
            email="",
            phone="",
            address="",
            city="",
            state="",
            country=""
        )

        # 創建訂單項目
        # 多個商品關聯到一個訂單id
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )

        # 清空購物車
        cart_items.delete()

        # 直接導向到綠界付款頁面
        return redirect('ecpay_payment', order_id=order.id)
    except Cart.DoesNotExist:
        return redirect('cart')

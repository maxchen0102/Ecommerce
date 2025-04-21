from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .decorators import seller_required
from .forms import ProductForm
from store.models import Product, Order, OrderItem


@seller_required
def dashboard(request):
    """賣家儀表板"""
    # 獲取賣家的商品
    products = Product.objects.filter(seller=request.user)

    # 獲取包含賣家商品的訂單
    seller_products = Product.objects.filter(seller=request.user)
    order_items = OrderItem.objects.filter(product__in=seller_products)
    recent_orders = Order.objects.filter(
        items__in=order_items).distinct().order_by('-created_at')[:5]

    context = {
        'products': products,
        'recent_orders': recent_orders,
    }
    return render(request, 'seller/dashboard.html', context)


@seller_required
def product_list(request):
    """賣家商品列表"""
    products = Product.objects.filter(seller=request.user)

    context = {
        'products': products,
    }
    return render(request, 'seller/product_list.html', context)


@seller_required
def add_product(request):
    """新增商品"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f'商品 {product.name} 已成功新增！')
            return redirect('seller:product_list')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': '新增商品'
    }
    return render(request, 'seller/product_form.html', context)


@seller_required
def edit_product(request, product_id):
    """編輯商品"""
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'商品 {product.name} 已成功更新！')
            return redirect('seller:product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'title': '編輯商品'
    }
    return render(request, 'seller/product_form.html', context)


@seller_required
def delete_product(request, product_id):
    """刪除商品"""
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'商品 {product_name} 已成功刪除！')
        return redirect('seller:product_list')

    context = {
        'product': product
    }
    return render(request, 'seller/delete_product.html', context)


@seller_required
def order_list(request):
    """賣家訂單列表"""
    # 獲取包含賣家商品的所有訂單
    seller_products = Product.objects.filter(seller=request.user)
    order_items = OrderItem.objects.filter(product__in=seller_products)
    orders = Order.objects.filter(
        items__in=order_items).distinct().order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'seller/order_list.html', context)

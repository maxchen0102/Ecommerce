from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm
from .models import UserProfile
from store.models import Order


def register(request):
    """用戶註冊視圖"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 創建用戶資料並保存電話
            phone = form.cleaned_data.get('phone')
            user_profile = UserProfile.objects.create(user=user, phone=phone)
            # 自動登入用戶
            login(request, user)
            messages.success(request, '註冊成功！歡迎加入我們的購物網站。')
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def user_login(request):
    """用戶登入視圖"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # 獲取登入後要導向的頁面
            next_page = request.GET.get('next', 'home')
            messages.success(request, '登入成功！')
            return redirect(next_page)
        else:
            messages.error(request, '用戶名或密碼錯誤，請重試。')

    return render(request, 'account/login.html')


def user_logout(request):
    """用戶登出視圖"""
    logout(request)
    messages.success(request, '您已成功登出！')
    return redirect('home')


@login_required
def profile(request):
    """用戶資料視圖"""
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        # 如果用戶資料不存在，創建一個
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, '個人資料已更新！')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # 取得用戶的訂單
    orders = Order.objects.filter(
        email=request.user.email).order_by('-created_at')

    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, 'account/profile.html', context)

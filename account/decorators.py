from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def seller_required(view_func):
    """
    Decorator for views that checks that the user is a seller,
    redirecting to the login page if necessary.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, '請先登入')
            return redirect('login')

        try:
            if not request.user.profile.is_seller:
                messages.error(request, '您沒有賣家權限')
                return redirect('home')
        except:
            messages.error(request, '用戶資料不完整')
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view

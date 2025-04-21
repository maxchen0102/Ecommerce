from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用戶資料'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_seller')
    list_select_related = ('profile', )

    def is_seller(self, obj):
        try:
            return obj.profile.is_seller
        except:
            return False

    is_seller.short_description = '賣家'
    is_seller.boolean = True


# 重新註冊User模型
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# 直接註冊UserProfile模型


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_seller')
    list_filter = ('is_seller',)
    search_fields = ('user__username', 'user__email', 'phone')

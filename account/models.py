from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(
        upload_to='users/', blank=True, null=True)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

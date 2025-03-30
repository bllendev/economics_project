from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm


User = get_user_model()


class UserAdmin(UserAdmin):
    pass


admin.site.register(User, UserAdmin)

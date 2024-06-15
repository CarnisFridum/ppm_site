from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ProfilePic

class ProfilePicInline(admin.StackedInline):
    model = ProfilePic
    can_delete = False
    verbose_name_plural = "profilePic"

class UserWithPic(BaseUserAdmin):
    inlines = [ProfilePicInline]

admin.site.unregister(User)
admin.site.register(User, UserWithPic)
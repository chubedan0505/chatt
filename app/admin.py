from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
admin.site.register([UserSession])
admin.site.register([Profile])
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_active',)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
class CustomUserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('is_active',)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ConfirmationCode)
admin.site.register(Message)
admin.site.register(FriendInvitation)
admin.site.register(Friendship)
admin.site.register(FriendRequest)



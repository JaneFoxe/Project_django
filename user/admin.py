from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка юзера"""
    list_display = ('email', 'phone', 'country',)
    list_filter = ('email', 'country',)
    search_fields = ('email', 'country',)

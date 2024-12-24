from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'password', 'email',
        'phone_number', 'city', 'avatar'
    )


admin.site.register(User, UserAdmin)
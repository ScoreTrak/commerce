from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ldfinance.users import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("date_joined", "last_login")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("username",)
    list_display = ("username", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    filter_horizontal = ("groups", "user_permissions")

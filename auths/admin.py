from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from auths.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # filter_horizontal = ('refer_parent',)

    list_display = [
        "email",
        "username",
        "is_active",
        "is_superuser",
        "team_lead",
    ]
    list_filter = ["is_active", "is_superuser",]
    readonly_fields = ["date_joined"]
    search_fields = ["email", "username",]
    fieldsets = (
        (None, {"fields": ("email", "username", "password",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "team_lead",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",

                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined",)}),
    )

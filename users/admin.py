from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


@admin.register(User)
class UserModelAdmin(UserAdmin, ModelAdmin):
    list_display = ["phone", "first_name", "last_name", "balance", "city", "town", "school"]

    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    add_fieldsets = (
        (
            "Ma'lumotlar", {
                "fields": (
                    "phone", "first_name", "last_name",
                )
            }
        ),
        (
            "Joylashuv", {
                "fields": (
                    "city", "town", "village", "school",
                )
            }
        ),
        (
            "Qo'shimcha", {
                "fields": (
                    "role", "image",
                )
            }
        )
    )

    fieldsets = (
        (
            "Ma'lumotlar", {
                "fields": (
                    "phone", "first_name", "last_name",
                )
            }
        ),
        (
            "Joylashuv", {
                "fields": (
                    "city", "town", "village", "school",
                )
            }
        ),
        (
            "Qo'shimcha", {
                "fields": (
                    "role", "image",
                )
            }
        )
    )

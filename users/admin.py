from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


from .models import User, Transaction, Group


@admin.register(Token)
class TokenAdmin(ModelAdmin):
    list_display = ('key', 'user', 'created')
    search_fields = ('key', 'user__username')


@admin.register(User)
class UserModelAdmin(UserAdmin, ModelAdmin):
    list_display = [
        "phone",
        "first_name",
        "last_name",
        "balance",
        "city",
        "town",
        "school",
        "role",
    ]
    ordering = ["phone"]
    list_filter = [
        "city",
        "town",
        "role",
    ]
    search_fields = [
        "phone",
        "first_name",
        "last_name",
    ]

    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    add_fieldsets = (
        (
            "Ma'lumotlar",
            {
                "fields": (
                    "phone",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                )
            },
        ),
        (
            "Joylashuv",
            {
                "fields": (
                    "city",
                    "town",
                    "village",
                    "school",
                )
            },
        ),
        (
            "Qo'shimcha",
            {
                "fields": (
                    "role",
                    "image",
                )
            },
        ),
    )

    fieldsets = (
        (
            "Ma'lumotlar",
            {
                "fields": (
                    "phone",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Joylashuv",
            {
                "fields": (
                    "city",
                    "town",
                    "village",
                    "school",
                )
            },
        ),
        (
            "Qo'shimcha",
            {
                "fields": (
                    "role",
                    "image",
                )
            },
        ),
    )


@admin.register(Transaction)
class TransactionModelAdmin(ModelAdmin):
    list_display = [
        "author",
        "type",
        "tid",
        "service",
        "description",
        "amount",
        "state",
        "created",
    ]


@admin.register(Group)
class GroupModelAdmin(ModelAdmin):
    list_display = [
        "name",
        "teacher",
        "count_members",
    ]

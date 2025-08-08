from django.urls import path

from .views import (
    login,
    signup,
    delete,

    profile,
    edit_profile,
    get_transactions,
    get_groups,

    payme_callback,
)


urlpatterns = [
    path("auth/login/", login),
    path("auth/signup/", signup),
    path("auth/delete/", delete),

    path("auth/profile/", profile),
    path("auth/profile/edit/", edit_profile),
    path("auth/transactions/", get_transactions),
    path("groups/", get_groups),

    path("payme_callback/", payme_callback),
]

from django.urls import path

from .views import (
    login,
    signup,
    delete,

    profile,
    edit_profile,
    get_invites,
    accept_invite,
    
    create_group,
    get_students,
    invite_members,

    payme_callback,
)


urlpatterns = [
    path("auth/login/", login),
    path("auth/signup/", signup),
    path("auth/delete/", delete),

    path("auth/profile/", profile),
    path("auth/profile/edit/", edit_profile),
    path("auth/profile/invites/", get_invites),
    path("auth/profile/invites/accept/", accept_invite),

    path("teacher/group/create/", create_group),
    path("teacher/students/", get_students),
    path("teacher/group/invite/", invite_members),

    path("payme_callback/", payme_callback),
]

from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import decorators
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from utils.worker import Worker

from .models import User, Group, Invite
from .serializers import (
    UserSerializer,
    UserEditSerializer,
    StudentsSerializer,
    InvitesSerializer,
)


@decorators.api_view(http_method_names=["POST"])
def signup(request: HttpRequest):
    phone = request.data.get("phone")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    city = request.data.get("city")
    town = request.data.get("town")
    village = request.data.get("village")
    school = request.data.get("school")
    password = request.data.get("password")

    if not phone:
        return Response(
            {"status": "error", "error": "phone_required", "data": None}, status=400
        )

    if not first_name:
        return Response(
            {"status": "error", "error": "first_name_required", "data": None},
            status=400,
        )

    if not last_name:
        return Response(
            {"status": "error", "error": "last_name_required", "data": None}, status=400
        )

    if not city:
        return Response(
            {"status": "error", "code": "city_required", "data": None}, status=400
        )

    if not town:
        return Response(
            {"status": "error", "error": "town_required", "data": None}, status=400
        )

    if not village:
        return Response(
            {"status": "error", "error": "village_required", "data": None}, status=400
        )

    if not school:
        return Response(
            {"status": "error", "error": "scholl_required", "data": None}, status=400
        )

    if not password:
        return Response({"status": "error", "error": "password_required", "data": None})

    user = User.objects.filter(phone=phone)

    if user.exists():
        return Response(
            {"status": "error", "error": "phone_exists", "data": None}, status=400
        )

    user = User.objects.create(
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        city=city,
        town=town,
        village=village,
        school=school,
    )

    user.set_password(raw_password=password)
    user.save()

    return Response({"status": "success", "error": None, "data": None})


@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    phone = request.data.get("phone")
    password = request.data.get("password")

    user = User.objects.filter(phone=phone)

    if not user.exists():
        return Response(
            {"status": "error", "error": "phone_not_found", "data": None}, status=400
        )

    user = user.first()

    if not user.check_password(raw_password=password):
        return Response(
            {"status": "error", "error": "password_didnot_match", "data": None}
        )

    token = Token.objects.get_or_create(user=user)

    return Response(
        {
            "status": "success",
            "error": None,
            "data": {
                **UserSerializer(user).data,
                "token": token[0].key,
            },
        }
    )


@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def delete(request: HttpRequest):
    user: User = request.user
    user.delete()
    return Response({"status": "success", "error": None, "data": None})


@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def profile(request: HttpRequest):
    user: User = request.user

    return Response(
        {"status": "success", "error": None, "data": UserSerializer(user).data}
    )


@decorators.api_view(http_method_names=["POST"])
def edit_profile(request: HttpRequest):
    user = request.user
    data = request.data

    user_serializer = UserEditSerializer(user, data=data)

    if user_serializer.is_valid():
        user_serializer.save()
        return Response({"status": "success", "error": None, "data": None})

    return Response({"status": "error", "error": "fill_empty_fields", "data": None})


@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def get_invites(request: HttpRequest):
    user: User = request.user
    invites = Invite.objects.filter(student=user)
    invites_serializer = InvitesSerializer(invites, many=True).data
    return Response(
        {"status": "success", "error": None, "data": {"invites": invites_serializer}}
    )


@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def accept_invite(request: HttpRequest):
    user: User = request.user
    invite = request.data.get("invite")

    if not invite:
        return Response(
            {"status": "error", "error": "invite_required", "data": None}, status=400
        )

    invite = Invite.objects.filter(pk=invite)

    if not invite.exists():
        return Response({"status": "error", "error": "invite_not_found", "data": None})

    invite = invite.first()

    invite.group.members.add(user)
    invite.group.save()

    return Response({"status": "success", "error": None, "data": None})


# Teacher endpoints
# get students list
@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def get_students(request: HttpRequest):
    students = User.objects.filter(role="student")
    students_serializer = StudentsSerializer(students, many=True).data
    return Response(
        {"status": "success", "error": None, "data": {"students": students_serializer}}
    )


# create new group
@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def create_group(request: HttpRequest):
    user: User = request.user
    name = request.data.get("name")

    if not name:
        return Response(
            {"status": "error", "error": "name_required", "data": None}, status=400
        )

    Group.objects.create(teacher=user, name=name)
    return Response({"status": "success", "error": None, "data": None})


# invite members for group
@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def invite_members(request: HttpRequest):
    group = request.data.get("group")
    students = request.data.get("students", [])

    if not group:
        return Response(
            {"status": "error", "error": "group_required", "data": None}, status=400
        )

    if not students:
        return Response(
            {"status": "error", "error": "students_required", "data": None}, status=400
        )

    if not isinstance(students, list):
        return Response({"status": "error", "error": "students_invalid", "data": None})

    group = Group.objects.filter(id=group)

    if not group.exists():
        return Response(
            {"status": "error", "error": "group_not_found", "data": None}, status=400
        )

    group = group.first()

    worker = Worker(
        lambda students, group: [
            Invite.objects.create(student=s, group=group)
            for s in User.objects.filter(pk__in=students, role="student")
        ],
        students=students,
        group=group,
    )

    worker.start()

import json
import time
from drf_yasg import openapi
from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from utils.worker import Worker

from .models import User, Group, Transaction
from .serializers import (
    UserSerializer,
    UserEditSerializer,
    StudentsSerializer,
    SignUpBodySerializer,
    LoginBodySerializer,
    EditProfileSerializer,
    GroupSerializer,
    TransactionSerializer
)


@swagger_auto_schema(
    method="get",
    operation_description="Guruhlar ro'yxati",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
@decorators.api_view(http_method_names=["GET"])
def get_groups(request: HttpRequest):
    groups = Group.objects.all()
    return Response(
        {
            "status": "success",
            "error": None,
            "data": GroupSerializer(groups, many=True).data,
        }
    )


@swagger_auto_schema(
    method="get",
    operation_description="Tranzaksiyalar ro'yxati",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def get_transactions(request: HttpRequest):
    user = request.user
    transactions = Transaction.objects.filter(author=user)
    return Response(
        {
            "status": "success",
            "error": None,
            "data": TransactionSerializer(transactions, many=True).data,
        }
    )



@swagger_auto_schema(
    method="post",
    operation_description="SignUp endpoint",
    request_body=SignUpBodySerializer,
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


@swagger_auto_schema(
    method="post",
    operation_description="Login endpoint",
    request_body=LoginBodySerializer,
)
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



@swagger_auto_schema(
    method="post",
    operation_description="Delete account endpoint",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def delete(request: HttpRequest):
    user: User = request.user
    user.delete()
    return Response({"status": "success", "error": None, "data": None})


@swagger_auto_schema(
    method="get",
    operation_description="Profile endpoint",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def profile(request: HttpRequest):
    user: User = request.user

    return Response(
        {"status": "success", "error": None, "data": UserSerializer(user).data}
    )



@swagger_auto_schema(
    method="post",
    operation_description="Edit profile endpoint",
    request_body=EditProfileSerializer,
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def edit_profile(request: HttpRequest):
    user = request.user
    data = request.data

    user_serializer = UserEditSerializer(user, data=data)

    if user_serializer.is_valid():
        user_serializer.save()
        return Response({"status": "success", "error": None, "data": None})

    return Response({"status": "error", "error": "fill_empty_fields", "data": None})


# PayMe callback handler for payments
@swagger_auto_schema(method="post", auto_schema=None)
@decorators.api_view(http_method_names=["POST"])
def payme_callback(request: HttpRequest):
    user: User = None

    body = json.loads(request.body.decode())
    print(body)

    if body.get("method") == "CheckPerformTransaction":
        account_phone = body.get("params", {}).get("account", {}).get("id", "")

        user = User.objects.filter(phone=account_phone)

        if not user.exists():
            return Response(
                {
                    "error": {
                        "code": -31050,
                        "message": {
                            "uz": "Telefon raqami bog'langan hisob topilmadi. Birinchi ilovadan ro'yxatdan o'ting",
                        },
                        "data": "id",
                    }
                }
            )

        user = user.first()

        return Response(
            {
                "jsonrpc": "2.0",
                "id": "1",
                "result": {
                    "allow": True,
                },
            }
        )

    if body.get("method") == "CreateTransaction":
        account_phone = body.get("params", {}).get("account", {}).get("id", "")
        tid = body.get("params", {}).get("id")
        amount = body.get("params", {}).get("amount", 1) / 100

        user = User.objects.filter(phone=account_phone).first()
        transaction = Transaction.objects.create(
            author=user, tid=tid, amount=amount, state=1
        )

        return Response(
            {
                "result": {
                    "create_time": body.get("params").get("time"),
                    "transaction": transaction.tid,
                    "state": transaction.state,
                }
            }
        )

    if body.get("method") == "PerformTransaction":
        tid = body.get("params", {}).get("id")

        transaction = Transaction.objects.filter(tid=tid)

        if not transaction.exists():
            return Response(
                {
                    "error": {
                        "code": -31003,
                    }
                }
            )

        transaction = transaction.first()
        transaction.author.balance = transaction.amount
        transaction.author.save()
        transaction.state = 2
        transaction.save()

        return Response(
            {
                "result": {
                    "transaction": tid,
                    "perform_time": int(time.time()),
                    "state": 2,
                }
            }
        )

    return Response({})

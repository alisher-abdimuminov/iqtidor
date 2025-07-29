from drf_yasg import openapi
from rest_framework import generics
from django.http import HttpRequest
from rest_framework import decorators
from datetime import datetime, timedelta
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

from users.models import User

from .models import (
    Dtm,
    Cefr,
    Subject,
    Banner,
    DTMResult,
    CEFRResult,
)
from .serializers import (
    DtmsSerializer,
    DtmSerializer,
    CefrSerializer,
    CefrsSerializer,
    SubjectSerializer,
    BannerSerializer,
)


class BannersListAPIView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class SubjectsListAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.append(
            {"id": 0, "name": "dtm", "count_dtms": Dtm.objects.count()}
        )
        return response


class DtmsListAPIView(generics.ListAPIView):
    queryset = Dtm.objects.all()
    serializer_class = DtmsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


@swagger_auto_schema(
    method="get",
    operation_description="DTM ni olish",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
)
@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def get_dtm(request: HttpRequest, pk: int):
    user = request.user
    dtm_obj = Dtm.objects.filter(pk=pk)

    if not dtm_obj.exists():
        return Response(
            {"status": "error", "error": "dtm_not_found", "data": None}, status=404
        )

    dtm_obj = dtm_obj.first()

    if not dtm_obj.is_public and user not in dtm_obj.participants.all():
        return Response({"status": "error", "error": "dtm_is_private", "data": None})

    return Response(
        {
            "status": "success",
            "error": None,
            "data": {**DtmSerializer(dtm_obj, context={"request": request}).data},
        }
    )


@swagger_auto_schema(
    method="post",
    operation_description="DTM ni sotib olish",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
)
@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def purchase_dtm(request: HttpRequest, pk: int):
    user: User = request.user
    dtm_obj = Dtm.objects.filter(pk=pk)

    if not dtm_obj.exists():
        return Response(
            {"status": "error", "error": "dtm_not_found", "data": None}, status=404
        )

    dtm_obj = dtm_obj.first()

    if dtm_obj.group:
        return Response({"status": "error", "error": "dtm_for_group", "data": None})

    if not dtm_obj.is_public and (user not in dtm_obj.participants.all()):
        if dtm_obj.price <= user.balance:
            user.balance = user.balance - dtm_obj.price
            user.save()
            dtm_obj.participants.add(user)
            dtm_obj.save()
            return Response({"status": "success", "error": None, "data": None})
        else:
            return Response(
                {"status": "error", "error": "balance_is_not_enough", "data": None}
            )
    else:
        dtm_obj.participants.add(user)
        dtm_obj.save()

    return Response(
        {"status": "error", "error": "dtm_is_public_or_purchased", "data": None}
    )


# cefr
class CefrListAPIView(generics.ListAPIView):
    queryset = Cefr.objects.all()
    serializer_class = CefrsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subject"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


@swagger_auto_schema(
    method="get",
    operation_description="CEFR ni olish",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
)
@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def get_cefr(request: HttpRequest, pk: int):
    cefr_obj = Cefr.objects.filter(pk=pk)

    if not cefr_obj.exists():
        return Response(
            {"status": "error", "error": "cefr_not_found", "data": None}, status=404
        )

    cefr_obj = cefr_obj.first()

    return Response(
        {
            "status": "success",
            "error": None,
            "data": {**CefrSerializer(cefr_obj, context={"request": request}).data},
        }
    )


@swagger_auto_schema(
    method="post",
    operation_description="CEFR ni sotib olish",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
)
@decorators.api_view(http_method_names=["POST"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def purchase_cefr(request: HttpRequest, pk: int):
    user: User = request.user
    cefr_obj = Cefr.objects.filter(pk=pk)

    if not cefr_obj.exists():
        return Response(
            {"status": "error", "error": "cefr_not_found", "data": None}, status=404
        )

    cefr_obj = cefr_obj.first()

    if cefr_obj.group:
        return Response({"status": "error", "error": "cefr_for_group", "data": None})

    if not cefr_obj.is_public and (user not in cefr_obj.participants.all()):
        if cefr_obj.price <= user.balance:
            user.balance = user.balance - cefr_obj.price
            user.save()
            cefr_obj.participants.add(user)
            cefr_obj.save()
            return Response({"status": "success", "error": None, "data": None})
        else:
            return Response(
                {"status": "error", "error": "balance_is_not_enough", "data": None}
            )
    else:
        cefr_obj.participants.add(user)
        cefr_obj.save()

    return Response(
        {"status": "error", "error": "cefr_is_public_or_purchased", "data": None}
    )


@swagger_auto_schema(
    method="get",
    operation_description="Profile statistikasi",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
)
@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def get_statistics(request: HttpRequest):
    user = request.user
    now = datetime.now()
    filter_by = request.GET.get("filter_by")

    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    dtms = DTMResult.objects.all()

    if filter_by == "monthly":
        dtms = DTMResult.objects.filter(
            created__year=now.year, created__month=now.month, author=user
        )
    elif filter_by == "weekly":
        dtms = DTMResult.objects.filter(
            created__date__gte=start_of_week.date(),
            created__date__lte=end_of_week.date(),
            author=user,
        )

    cefrs = CEFRResult.objects.all()

    if filter_by == "monthly":
        cefrs = CEFRResult.objects.filter(
            created__year=now.year, created__month=now.month
        )
    elif filter_by == "weekly":
        cefrs = CEFRResult.objects.filter(
            created__date__gte=start_of_week.date(),
            created__date__lte=end_of_week.date(),
        )

    return Response(
        {
            "status": "success",
            "error": None,
            "data": {
                "dtms": dtms.count(),
                "passed_dtms": dtms.filter(status="passed").count(),
                "cefrs": cefrs.count(),
                "passed_cefrs": cefrs.filter(status="passed").count(),
            },
        }
    )


@swagger_auto_schema(
    method="get",
    operation_description="Search",
    request_body=None,
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="Token",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
)
@decorators.api_view(http_method_names=["GET"])
@decorators.authentication_classes(authentication_classes=[TokenAuthentication])
@decorators.permission_classes(permission_classes=[IsAuthenticated])
def search(request: HttpRequest, search: str):
    search = search.strip()
    dtms = Dtm.objects.filter(name__icontains=search)
    cefr = Cefr.objects.filter(name__icontains=search)
    print(search)
    print(dtms.count())
    print(cefr.count())
    return Response({
        "status": "success",
        "error": None,
        "data": {
            "dtms": DtmsSerializer(dtms, many=True, context={ "request": request }).data,
            "cefrs": CefrsSerializer(cefr, many=True, context={ "request": request }).data
        }
    })
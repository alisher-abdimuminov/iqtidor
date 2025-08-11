from uuid import uuid4
from drf_yasg import openapi
from rest_framework import generics
from django.http import HttpRequest
from rest_framework import decorators
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

from users.models import User, Transaction, Group
from utils.generate_answers_sheet import generate_answers_sheet

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
            Transaction.objects.create(
                author=user,
                type="expense",
                tid=str(uuid4()),
                service="purchase_dtm",
                description=dtm_obj.name,
                state=3,
                amount=dtm_obj.price,
            )
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
            Transaction.objects.create(
                author=user,
                type="expense",
                tid=str(uuid4()),
                service="purchase_cefr",
                description=cefr_obj.name,
                state=3,
                amount=cefr_obj.price,
            )
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
    return Response(
        {
            "status": "success",
            "error": None,
            "data": {
                "dtms": DtmsSerializer(
                    dtms, many=True, context={"request": request}
                ).data,
                "cefrs": CefrsSerializer(
                    cefr, many=True, context={"request": request}
                ).data,
            },
        }
    )


@swagger_auto_schema(
    method="post",
    operation_description="DTM natijalarin saqlash",
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
def save_dtm_result(request: HttpRequest, pk: int):
    user: User = request.user
    points = request.data.get("points", 0)
    status = "failed"
    cases = request.data.get("cases")
    teacher = request.data.get("teacher")

    dtm = Dtm.objects.filter(pk=pk)
    teacher = User.objects.filter(pk=teacher)

    if not dtm:
        return Response({"status": "error", "error": "dtm_not_found", "data": None})

    if not teacher:
        return Response({"status": "error", "error": "teacher_not_found", "data": None})

    dtm = dtm.first()
    teacher = teacher.first()

    dtm_result = DTMResult.objects.filter(author=user, dtm=dtm)

    if dtm_result:
        return Response(
            {"status": "error", "error": "dtm_already_solved", "data": None}
        )

    if points < dtm.passing_score:
        status = "passed"

    result = DTMResult.objects.create(
        author=user,
        teacher=teacher,
        dtm=dtm,
        cases=cases,
        points=points,
        status=status,
    )

    result.answers_sheet.save(
        f"{user.first_name} {user.last_name}.pdf",
        ContentFile(
            generate_answers_sheet(
                answers=result.cases.get("answers", ""),
                keys=result.cases.get("keys", ""),
                student=f"{user.first_name} {user.last_name}",
                score=result.points,
                date=result.created.strftime("%d/%m/%Y"),
                groups=(
                    ("Blok 1", 1, 10),
                    ("Blok 2", 11, 20),
                    ("Blok 3", 21, 30),
                    ("Blok 4", 31, 60),
                    ("Blok 4", 61, 90),
                ),
            ),
            f"{user.first_name} {user.last_name}.pdf",
        ),
    )

    return Response({"status": "success", "error": None, "data": None})


@swagger_auto_schema(
    method="post",
    operation_description="DTM natijalarin saqlash",
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
def save_cefr_result(request: HttpRequest, pk: int):
    user: User = request.user
    cases = request.data.get("cases")
    teacher = request.data.get("teacher")

    cefr = Cefr.objects.filter(pk=pk)
    teacher = User.objects.filter(pk=pk)

    if not cefr:
        return Response({"status": "error", "error": "cefr_not_found", "data": None})
    
    if not teacher:
        return Response({"status": "error", "error": "teacher_not_found", "data": None})

    cefr = cefr.first()
    teacher = teacher.first()


    cefr_result = CEFRResult.objects.filter(author=user, cefr=cefr)

    if cefr_result:
        return Response(
            {"status": "error", "error": "cefr_already_solved", "data": None}
        )

    CEFRResult.objects.create(
        author=user,
        cefr=cefr,
        cases=cases,
        teacher=teacher,
    )

    return Response({"status": "success", "error": None, "data": None})


@swagger_auto_schema(
    method="get",
    operation_description="Mening imtihonlarim",
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
def my_tests(request: HttpRequest):
    user: User = request.user

    dtms = Dtm.objects.filter(participants=user)
    cefrs = Cefr.objects.filter(participants=user)

    print("my request", request)
    return Response(
        {
            "status": "success",
            "error": None,
            "data": {
                "dtms": DtmsSerializer(
                    dtms, many=True, context={"request": request}
                ).data,
                "cefrs": CefrsSerializer(
                    cefrs, many=True, context={"request": request}
                ).data,
            },
        }
    )


@swagger_auto_schema(
    method="get",
    operation_description="DTM statistika",
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
def dtm_statistics(request: HttpRequest, pk: int):
    dtm = Dtm.objects.filter(pk=pk)

    if not dtm:
        return Response({"status": "error", "error": "dtm_not_found", "data": None})

    dtm = dtm.first()

    top_results = DTMResult.objects.order_by('-points', '-created').values('author__id', 'author__first_name', 'author__last_name', 'points', 'status')

    groups_ranked = (
        Group.objects
        .annotate(total_points=Sum('members__dtmresult__points'))
        .order_by('-total_points', 'name')
        .values('id', 'name', 'total_points')
    )

    teachers_ranked = (
        DTMResult.objects
        .values('teacher__id', 'teacher__first_name', 'teacher__last_name', 'teacher__phone')
        .annotate(total_points=Sum('points'), result_count=Count('id'))
        .order_by('-total_points', '-result_count')
        .values('teacher__id', 'teacher__first_name', 'teacher__last_name')
    )

    return Response({
        "status": "success",
        "error": None,
        "data": {
            "by_point": list(top_results),
            "by_group": list(groups_ranked),
            "by_teacher": list(teachers_ranked)
        }
    })


@swagger_auto_schema(
    method="get",
    operation_description="CEFR statistika",
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
def cefr_statistics(request: HttpRequest, pk: int):
    cefr = Cefr.objects.filter(pk=pk)

    if not cefr:
        return Response({"status": "error", "error": "cefr_not_found", "data": None})

    cefr = cefr.first()

    top_results = CEFRResult.objects.order_by('-rash', '-created').values('author__id', 'author__first_name', 'author__last_name', 'rash', 'degree')

    groups_ranked = (
        Group.objects
        .annotate(total_points=Sum('members__cefrresult__rash'))
        .order_by('-total_points', 'name')
        .values('id', 'name', 'total_points')
    )

    teachers_ranked = (
        User.objects
        .annotate(total_points=Sum('rash'), result_count=Count('id'))
        .order_by('-total_points', '-result_count')
        .values('teacher__id', 'teacher__first_name', 'teacher__last_name')
    )

    return Response({
        "status": "success",
        "error": None,
        "data": {
            "by_point": list(top_results),
            "by_group": list(groups_ranked),
            "by_teacher": list(teachers_ranked)
        }
    })


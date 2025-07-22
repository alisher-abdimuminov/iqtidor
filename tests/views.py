from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import decorators
from rest_framework import generics


from .models import (
    Dtm,
    Cefr,
    Subject,
)
from .serializers import (
    DtmsSerializer,
    DtmSerializer,
    CefrSerializer,
    CefrsSerializer,
    SubjectSerializer,
)


class SubjectsListAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.append({
            "id": 0,
            "name": "dtm",
            "count_dtms": Dtm.objects.count()
        })
        return response


class DtmsListAPIView(generics.ListAPIView):
    queryset = Dtm.objects.all()
    serializer_class = DtmsSerializer


@decorators.api_view(http_method_names=["GET"])
def get_dtm(request: HttpRequest, pk: int):
    dtm_obj = Dtm.objects.filter(pk=pk)

    if not dtm_obj.exists():
        return Response({
            "status": "error",
            "error": "dtm_not_found",
            "data": None
        }, status=404)
    
    dtm_obj = dtm_obj.first()

    return Response({
        "status": "success",
        "error": None,
        "data": {
            **DtmSerializer(dtm_obj, context={ "request": request }).data
        }
    })


@decorators.api_view(http_method_names=["POST"])
def join_dtm(request: HttpRequest, pk):
    dtm_obj = Dtm.objects.filter(pk=pk)

    if not dtm_obj.exists():
        return Response({
            "status": "error",
            "error": "dtm_not_found",
            "data": None
        }, status=404)
    
    dtm_obj = dtm_obj.first()

    dtm_obj.participants.add(request.user)
    dtm_obj.save()

    return Response({
        "status": "success",
        "error": None,
        "data": None
    })


# cefr
class CefrListAPIView(generics.ListAPIView):
    queryset = Cefr.objects.all()
    serializer_class = CefrsSerializer


@decorators.api_view(http_method_names=["GET"])
def get_cefr(request: HttpRequest, pk: int):
    cefr_obj = Cefr.objects.filter(pk=pk)

    if not cefr_obj.exists():
        return Response({
            "status": "error",
            "error": "cefr_not_found",
            "data": None
        }, status=404)
    
    cefr_obj = cefr_obj.first()

    return Response({
        "status": "success",
        "error": None,
        "data": {
            **CefrSerializer(cefr_obj, context={ "request": request }).data
        }
    })


@decorators.api_view(http_method_names=["POST"])
def join_cefr(request: HttpRequest, pk):
    cefr_obj = Cefr.objects.filter(pk=pk)

    if not cefr_obj.exists():
        return Response({
            "status": "error",
            "error": "cefr_not_found",
            "data": None
        }, status=404)
    
    cefr_obj = cefr_obj.first()

    cefr_obj.participants.add(request.user)
    cefr_obj.save()

    return Response({
        "status": "success",
        "error": None,
        "data": None
    })

from django.urls import path

from .views import (
    DtmsListAPIView,
    get_dtm,
    join_dtm,
    CefrListAPIView,
    get_cefr,
    join_cefr,
    SubjectsListAPIView,
)


urlpatterns = [
    path("subjects/", SubjectsListAPIView.as_view()),
    path("dtms/", DtmsListAPIView.as_view()),
    path("dtms/dtm/<int:pk>/", get_dtm),
    path("dtms/dtm/<int:pk>/join/", join_dtm),

    path("cefrs/", CefrListAPIView.as_view()),
    path("cefrs/cefr/<int:pk>/", get_cefr),
    path("cefrs/cefr/<int:pk>/join/", join_cefr),
]

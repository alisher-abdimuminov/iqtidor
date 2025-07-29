from django.urls import path

from .views import (
    DtmsListAPIView,
    get_dtm,
    CefrListAPIView,
    get_cefr,
    SubjectsListAPIView,
    BannersListAPIView,
    get_statistics,
    purchase_cefr,
    purchase_dtm,
    search,
    save_dtm_result,
    save_cefr_result,
    my_tests,
)


urlpatterns = [
    path("subjects/", SubjectsListAPIView.as_view()),
    path("banners/", BannersListAPIView.as_view()),

    path("dtms/", DtmsListAPIView.as_view()),
    path("dtms/dtm/<int:pk>/", get_dtm),
    path("dtms/dtm/<int:pk>/purchase/", purchase_dtm),
    path("dtms/dtm/<int:pk>/save/", save_dtm_result),

    path("cefrs/", CefrListAPIView.as_view()),
    path("cefrs/cefr/<int:pk>/", get_cefr),
    path("cefrs/cefr/<int:pk>/purchase/", purchase_cefr),
    path("cefrs/cefr/<int:pk>/save/", save_cefr_result),

    path("statistics/", get_statistics),
    path("search/<str:search>/", search),

    path("my/", my_tests),
]

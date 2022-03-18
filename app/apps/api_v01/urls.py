from django.urls import include, path

from rest_framework.routers import DefaultRouter


app_name = "api_v01"

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]

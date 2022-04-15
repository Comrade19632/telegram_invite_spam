from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import TelethonAccountsViewSet


app_name = "telethon_app"

router = DefaultRouter()

router.register("accounts", TelethonAccountsViewSet, basename="accounts")

urlpatterns = [
    path("", include(router.urls)),
]

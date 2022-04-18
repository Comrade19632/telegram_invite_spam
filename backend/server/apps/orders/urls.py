from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import InviteOrdersViewSet


app_name = "orders"

router = DefaultRouter()

router.register("invite", InviteOrdersViewSet, basename="invite-orders")

urlpatterns = [
    path("", include(router.urls)),
]

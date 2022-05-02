from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import InviteOrdersViewSet, SpamOrdersViewSet


app_name = "orders"

router = DefaultRouter()

router.register("invite", InviteOrdersViewSet, basename="invite-orders")
router.register("spam", SpamOrdersViewSet, basename="spam-orders")

urlpatterns = [
    path("", include(router.urls)),
]

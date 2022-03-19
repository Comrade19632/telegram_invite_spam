from django.urls import include, path

from rest_framework.routers import DefaultRouter

from apps.api_v01.views.customers import CustomerViewSet
from apps.api_v01.views.offers import OfferViewSet


app_name = "api_v01"

router = DefaultRouter()

router.register("offers", OfferViewSet, basename="offers")
router.register("customers", CustomerViewSet, basename="customers")

urlpatterns = [
    path("", include(router.urls)),
]

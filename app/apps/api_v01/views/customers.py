from rest_framework import mixins, viewsets

from apps.api_v01.serializers.customers_serializer import CustomerSerializer


class CustomerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CustomerSerializer

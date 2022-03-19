from rest_framework import viewsets

from apps.api_v01.serializers.offers_serializer import OfferSerializer
from apps.offers.models import Offer


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Offer.objects.filter(is_active=True)
    serializer_class = OfferSerializer

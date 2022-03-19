from rest_framework.serializers import ModelSerializer

from apps.offers.models import Offer


class OfferSerializer(ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            "id",
            "title",
            "my_order",
            "feature",
            "logo",
            "sum",
            "days",
            "interestRate",
            "time",
            "offerId",
        )

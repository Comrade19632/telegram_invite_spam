from rest_framework.serializers import ModelSerializer

from apps.customers.models import Customer


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "telegram_user_name",
            "telegram_chat_id",
            "phone_number",
        )

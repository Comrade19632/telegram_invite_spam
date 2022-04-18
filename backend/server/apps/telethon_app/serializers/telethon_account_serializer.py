from rest_framework.serializers import ModelSerializer

from apps.users.serializers import UserSerializer

from ..models import TelethonAccount


class TelethonAccountSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)

    def save(self, user, **kwargs):
        return super().save(owner=user, **kwargs)

    class Meta:
        model = TelethonAccount
        fields = (
            "id",
            "owner",
            "api_id",
            "api_hash",
            "phone_number",
            "is_initialized",
            "is_active",
            "created",
            "date_of_last_deactivate",
            "reason_of_last_deactivate",
        )

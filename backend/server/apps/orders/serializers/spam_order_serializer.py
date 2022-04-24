from rest_framework.serializers import ModelSerializer

from apps.users.serializers import UserSerializer

from ..models import SpamOrder


class SpamOrderSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    def save(self, user, **kwargs):
        return super().save(user=user, **kwargs)

    class Meta:
        model = SpamOrder
        fields = (
            "id",
            "user",
            "spam_message",
            "donor_chat_link",
            "affected_users",
            "created",
            "in_progress",
        )

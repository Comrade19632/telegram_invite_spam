from rest_framework.serializers import ModelSerializer

from apps.users.serializers import UserSerializer

from ..models import InviteOrder


class InviteOrderSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    def save(self, user, **kwargs):
        return super().save(user=user, **kwargs)

    class Meta:
        model = InviteOrder
        fields = (
            "id",
            "user",
            "target_chat_link",
            "donor_chat_link",
            "affected_users",
            "created",
            "in_progress",
        )

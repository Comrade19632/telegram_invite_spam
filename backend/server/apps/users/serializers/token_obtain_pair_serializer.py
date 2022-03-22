from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..serializers.user_serializer import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].required = False
        self.fields["telegram_id"].required = False

    def validate(self, attrs):
        attrs.update({"password": ""})
        attrs.update({"telegram_id": ""})
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({"user": UserSerializer(self.user).data})
        return data

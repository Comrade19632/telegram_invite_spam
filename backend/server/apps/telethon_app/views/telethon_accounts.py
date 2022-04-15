from rest_framework.viewsets import ModelViewSet

from ..models import TelethonAccount
from ..serializers import TelethonAccountSerializer


class TelethonAccountsViewSet(ModelViewSet):
    queryset = TelethonAccount.objects.all()
    serializer_class = TelethonAccountSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

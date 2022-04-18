from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
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

    @action(
        methods=["GET"],
        detail=True,
        url_name="activate",
        url_path="activate",
    )
    def activate_telethon_account(self, request, pk):
        account = self.get_object()
        account.is_active = True
        account.date_of_last_deactivate = None
        account.reason_of_last_deactivate = None
        account.save()
        return Response(status=HTTP_200_OK)

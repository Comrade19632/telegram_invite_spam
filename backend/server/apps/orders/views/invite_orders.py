from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from ..models import InviteOrder
from ..serializers import InviteOrderSerializer
from ..tasks import invite


class InviteOrdersViewSet(ModelViewSet):
    queryset = InviteOrder.objects.all()
    serializer_class = InviteOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["GET"],
        detail=True,
        url_name="start",
        url_path="start",
    )
    def start_invite_order(self, request, pk):
        order = self.get_object()
        if request.user == order.user:
            invite.delay(order.id)
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

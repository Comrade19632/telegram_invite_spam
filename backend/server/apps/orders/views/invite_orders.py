import django_filters.rest_framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from ..models import InviteOrder
from ..serializers import InviteOrderSerializer
from ..tasks import invite


class InviteOrdersViewSet(ModelViewSet):
    queryset = InviteOrder.objects.all()
    serializer_class = InviteOrderSerializer
    filter_fields = ["in_progress"]

    def get_queryset(self):
        queryset = super().get_queryset()

        target_chat_link = self.request.query_params.get("target_chat_link")
        donor_chat_link = self.request.query_params.get("donor_chat_link")

        if target_chat_link and donor_chat_link:
            return queryset.filter(
                user=self.request.user,
                target_chat_link=target_chat_link,
                donor_chat_link=donor_chat_link,
            )

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
        invite.delay(order.id)
        return Response(status=HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_name="stop",
        url_path="stop",
    )
    def stop_invite_order(self, request, pk):
        order = self.get_object()
        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)
        return Response(status=HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_name="merge-with-similar-orders",
        url_path="merge-with-similar-orders",
    )
    def megre_with_similar_orders(self, request, pk):
        order = self.get_object()
        for similar_order_id in request.data["similar_orders_ids"]:
            similar_order = InviteOrder.objects.get(id=similar_order_id)
            order.affected_users += similar_order.affected_users
            order.save()
        return Response(status=HTTP_200_OK)

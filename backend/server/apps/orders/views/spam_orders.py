import django_filters.rest_framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from ..models import SpamOrder
from ..serializers import SpamOrderSerializer
from ..tasks import spam


class SpamOrdersViewSet(ModelViewSet):
    queryset = SpamOrder.objects.all()
    serializer_class = SpamOrderSerializer
    filter_fields = ["in_progress"]

    def get_queryset(self):
        queryset = super().get_queryset()

        spam_message = self.request.query_params.get("spam_message")
        donor_chat_link = self.request.query_params.get("donor_chat_link")

        if spam_message and donor_chat_link:
            return queryset.filter(
                user=self.request.user,
                spam_message=spam_message,
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
    def start_spam_order(self, request, pk):
        order = self.get_object()
        order.in_progress = True
        order.save()
        spam.delay(order.id)
        return Response(status=HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_name="stop",
        url_path="stop",
    )
    def stop_spam_order(self, request, pk):
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
            similar_order = SpamOrder.objects.get(id=similar_order_id)
            order.affected_users += similar_order.affected_users
            order.save()
        return Response(status=HTTP_200_OK)

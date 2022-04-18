import asyncio

from aiogram import Bot

from server import celery_app

from ..models import InviteOrder
from ..services import invite as _invite


@celery_app.task(name="apps.orders.tasks.invite")
def invite(order_id):
    order = InviteOrder.objects.get(id=order_id)
    _invite(order)

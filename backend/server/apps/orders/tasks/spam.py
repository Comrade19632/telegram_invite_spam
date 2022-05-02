import asyncio

from aiogram import Bot

from server import celery_app

from ..models import SpamOrder
from ..services import spam as _spam


@celery_app.task(name="apps.orders.tasks.spam")
def spam(order_id):
    order = SpamOrder.objects.get(id=order_id)
    _spam(order)

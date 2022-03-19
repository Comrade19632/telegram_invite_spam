from zaim_server import celery_app

from ..services import SendMessage


@celery_app.task(name="apps.telegram_bot.tasks.send_message")
def send_message(chat_id, message):
    SendMessage(chat_id, message)()

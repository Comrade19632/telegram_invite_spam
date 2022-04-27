import csv
import datetime
import traceback

from django.conf import settings

from telethon.errors.common import MultiError
from telethon.errors.rpcerrorlist import InviteHashExpiredError, UserDeactivatedBanError
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import CheckChatInviteRequest, ImportChatInviteRequest
from telethon.tl.types import ChatInviteAlready

from apps.telegram_bot.tasks import send_message_to_user
from apps.telethon_app.models import TelethonAccount


def pars(order, loop=None):
    if order.user:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, is_busy=False, owner=order.user
        ).first()
    else:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, is_busy=False
        ).first()
    if not account:
        print("you dont have any active accounts")
        order.in_progress = False
        order.save()
        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "У вас не осталось активных аккаунтов",
            )
        return
    api_id = account.api_id
    api_hash = account.api_hash
    phone_number = account.phone_number
    account.is_busy = True
    account.save()

    client = TelegramClient(
        "telethon_sessions/" + str(phone_number), api_id, api_hash, loop=loop
    )

    try:
        client.connect()

    except:
        client.disconnect()
        traceback.print_exc()
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = (
            "Не удалось подключится, возможно аккаунт забанен"
        )
        account.save()
        pars(order.target_chat_link, order.user)

    try:
        chat = client.get_entity(order.target_chat_link)
        client(JoinChannelRequest(chat))
    except UserDeactivatedBanError:
        client.disconnect()
        print("account has been banned")
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = "Аккаунт был забанен навсегда"
        account.save()
        pars(order.target_chat_link, order.user)
    except ValueError:
        try:
            if isinstance(
                check_invite := client(CheckChatInviteRequest(order.target_chat_link)),
                ChatInviteAlready,
            ):
                chat = check_invite.chat
            else:
                updates = client(ImportChatInviteRequest(order.target_chat_link))
                chat = updates.chats[0]
        except InviteHashExpiredError:
            print("Недействительная ссылка на донор группу")
            order.in_progress = False
            order.save()
            account.is_busy = False
            account.save()
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    "Недействительная ссылка на донор группу",
                )
            return
    except:
        client.disconnect()
        traceback.print_exc()
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = (
            "Не удалось подключится, возможно аккаунт забанен"
        )
        account.save()
        pars(order.target_chat_link, order.user)

    all_participants = []

    try:
        all_participants = client.get_participants(chat, aggressive=False)
        client.disconnect()
    except TypeError:
        try:
            all_participants = client.get_participants(chat, aggressive=True)
            client.disconnect()
        except MultiError:
            client.disconnect()
            print("cannot pars channel")
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Не получилось спарсить канал"
            account.save()
            pars(order.target_chat_link, order.user)
        except:
            client.disconnect()
            print("cannot pars channel")
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Не получилось спарсить канал"
            account.save()
            pars(order.target_chat_link, order.user)

    except:
        client.disconnect()
        print("cannot pars channel")
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = "Не получилось спарсить канал"
        account.save()
        pars(order.target_chat_link, order.user)

    client.disconnect()

    with open(
        "pars_results/" + f"{account.api_id}{chat.id}.csv", "w+", encoding="UTF-8"
    ) as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerow(
            [
                "username",
                "user id",
                "access hash",
                "name",
                "group",
                "group id",
                "bot phone number",
            ]
        )
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + " " + last_name).strip()
            writer.writerow(
                [
                    username,
                    user.id,
                    user.access_hash,
                    name,
                    chat.title,
                    chat.id,
                    phone_number,
                ]
            )
        f.close()
        account.is_busy = False
        account.save()
        return f.name

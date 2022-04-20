import configparser
import csv
import datetime
import os
import sys
import time
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


def pars(target_chat_link, user_account=None, loop=None):
    if user_account:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, is_busy=False, owner=user_account
        ).first()
    else:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, is_busy=False
        ).first()
    if not account:
        print("you dont have any active accounts")
        if user_account:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                user_account.telegram_id,
                "У вас не осталось активных аккаунтов, заказ завершён",
            )
        return "fatal"
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
        pars(target_chat_link, user_account)
        return

    try:
        chat = client.get_entity(target_chat_link)
        client(JoinChannelRequest(chat))
    except UserDeactivatedBanError:
        client.disconnect()
        print("account has been banned")
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = "Аккаунт был забанен навсегда"
        account.save()
        pars(target_chat_link, user_account)
        return
    except ValueError:
        try:
            if isinstance(
                check_invite := client(CheckChatInviteRequest(target_chat_link)),
                ChatInviteAlready,
            ):
                chat = check_invite.chat
            else:
                updates = client(ImportChatInviteRequest(target_chat_link))
                chat = updates.chats[0]
        except InviteHashExpiredError:
            print("Недействительная ссылка на донор группу")
            account.is_busy = False
            account.save()
            if user_account:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    user_account.telegram_id,
                    "Недействительная ссылка на донор группу, заказ завершён",
                )
            return "fatal"
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
        pars(target_chat_link, user_account)
        return

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
            pars(target_chat_link, user_account)
            return
        except:
            client.disconnect()
            print("cannot pars channel")
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Не получилось спарсить канал"
            account.save()
            pars(target_chat_link, user_account)
            return

    except:
        client.disconnect()
        print("cannot pars channel")
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = "Не получилось спарсить канал"
        account.save()
        pars(target_chat_link, user_account)
        return

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

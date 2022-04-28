#!/usr/bin/env python3
import csv
import datetime
import random
import time
import traceback

from django.conf import settings

from telethon.errors.rpcerrorlist import (
    ChatAdminRequiredError,
    ChatWriteForbiddenError,
    FloodWaitError,
    PeerFloodError,
    UserBannedInChannelError,
    UserChannelsTooMuchError,
    UserDeactivatedBanError,
    UserIdInvalidError,
    UserKickedError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
)
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.types import InputPeerUser

from apps.orders.services.pars import pars
from apps.telegram_bot.tasks import send_message_to_user

from .get_account import get_account
from .get_or_create_eventloop import get_or_create_eventloop


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


def invite(order):
    order.in_progress = True
    order.save()

    loop = get_or_create_eventloop()

    input_file = pars(order, loop=loop)

    order.refresh_from_db()
    if not order.in_progress:
        print(re + "[+] Order has stopped")
        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "Заказ завершён",
            )
        return

    if not input_file:
        print(re + "[+] Order has stopped unexpectedly")

        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)

        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "Заказ завершён неожиданным образом",
            )
        return

    account = get_account(order)

    if not account:
        print("you dont have any active accounts")

        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)

        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "У вас не осталось активных или свободных аккаунтов, заказ завершён",
            )
        return

    order.telethon_accounts.add(account)
    account.is_busy = True
    account.save()

    api_id = account.api_id
    api_hash = account.api_hash
    phone_number = account.phone_number

    client = TelegramClient(
        "telethon_sessions/" + str(phone_number), api_id, api_hash, loop=loop
    )

    try:
        client.connect()

    except:
        client.disconnect()
        traceback.print_exc()
        account.is_active = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = (
            "Не удалось подключится, возможно аккаунт забанен"
        )
        account.is_busy = False
        account.save()
        invite(order)
        return

    print(f"Start with {phone_number} account")

    try:
        chat = client.get_entity(order.target_chat_link)
        client(JoinChannelRequest(chat))
    except ValueError:
        print("Недействительная ссылка на целевую группу")

        account.is_busy = False
        account.save()

        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)

        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                f"Недействительная ссылка на целевую группу, заказ завершён",
            )
        return

    if order.user:
        send_message_to_user.delay(
            settings.TELEGRAM_MANUAL_BOT_TOKEN,
            order.user.telegram_id,
            f"Успешно стартанул инвайт с аккаунта {phone_number}",
        )

    users = []
    with open(input_file, encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=";", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user["username"] = row[0]
            user["id"] = int(row[1])
            user["access_hash"] = int(row[2])
            user["name"] = row[3]
            users.append(user)

    for user in users:
        order.refresh_from_db()
        if not order.in_progress:
            print(re + "[+] Order has stopped")
            client.disconnect()
            account.is_busy = False
            account.save()
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    "Заказ завершён",
                )
            return
        if str(user["id"]) in order.affected_users:
            print(gr + "[+] This user already has been affected")
            continue
        order.affected_users.append(user["id"])
        order.save()
        try:
            user_to_add = InputPeerUser(user["id"], user["access_hash"])
            client(InviteToChannelRequest(chat, [user_to_add]))
            print(gr + "[+] Waiting for 10-30 Seconds...")
            time.sleep(random.randrange(10, 30))
        except FloodWaitError:
            client.disconnect()
            account.is_active = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Флуд, аккаунт временно заблокирован"
            account.is_busy = False
            account.save()
            print(
                re
                + "[!] Getting Flood Error from telegram. \n[!] Rerun function with another account"
            )
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} временно заблокирован, перезапускаем инвайт на другом аккаунте",
                )
            invite(order)
            return
        except PeerFloodError:
            client.disconnect()
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Флуд, аккаунт временно заблокирован"
            account.save()
            print(
                re
                + "[!] Getting Flood Error from telegram. \n[!] Rerun function with another account"
            )
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} временно заблокирован, перезапускаем инвайт на другом аккаунте",
                )
            invite(order)
            return
        except UserPrivacyRestrictedError:
            print(
                re
                + "[!] The user's privacy settings do not allow you to do this. Skipping."
            )
            continue
        except UserNotMutualContactError:
            print(re + "[!] The provided user is not a mutual contact. Skipping")
            continue
        except UserKickedError:
            print(re + "[!] This user was kicked from this channel. Skipping")
            continue
        except UserIdInvalidError:
            print(re + "[!] Invalid object ID for a user. Skipping")
            continue
        except UserChannelsTooMuchError:
            print(
                re
                + "[!] One of the users you tried to add is already in too many channels/supergroups"
            )
            continue
        except ChatWriteForbiddenError:
            client.disconnect()
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = (
                "Аккаунт был отключен, потому как не мог писать в чат донор"
            )
            account.save()
            print(re + "[!] Account can`t write in this chat")
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} не имеет права инвайтить в этот чат, перезапускаем инвайт на другом аккаунте",
                )
            invite(order)
            return
        except ChatAdminRequiredError:
            client.disconnect()
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = (
                "Аккаунт был отключен, потому как не мог писать в чат донор"
            )
            account.save()
            print(re + "[!] Account can`t write in this chat")
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} не имеет права инвайтить в этот чат, перезапускаем инвайт на другом аккаунте",
                )
            invite(order)
            return
        except UserBannedInChannelError:
            client.disconnect()
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = (
                "Аккаунт был отключен, потому как он забанен в данном канале"
            )
            account.save()
            print(re + "[!] Account can`t write in this chat")
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} забанен в данном канале, перезапускаем инвайт на другом аккаунте",
                )
            invite(order)
            return
        except UserDeactivatedBanError:
            client.disconnect()
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Аккаунт был забанен навсегда"
            account.save()
            print(re + "[!] Account can`t write in this chat")
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} забанен навсегда, перезапускаем инвайт на другом аккаунте",
                )
            invite(order)
            return
        except:
            client.disconnect()
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = (
                "Аккаунт был отключен по неизвестной причине"
            )
            account.save()
            traceback.print_exc()
            print(re + "[!] Unexpected Error")
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} был отключен по неизвестной причине, перезапускаем инвайт на другом аккаунте",
                )
            invite(order)
            return

    client.disconnect()

    order.in_progress = False
    order.save()
    order.telethon_accounts.update(is_busy=False)

    account.is_busy = False
    account.save()

    send_message_to_user.delay(
        settings.TELEGRAM_MANUAL_BOT_TOKEN,
        order.user.telegram_id,
        f"Заказ на инвайт успешно завершён",
    )

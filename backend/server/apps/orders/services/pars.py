import csv
import datetime
import traceback

from django.conf import settings

from telethon.errors.common import MultiError
from telethon.errors.rpcerrorlist import (
    ChannelPrivateError,
    InviteHashExpiredError,
    UserDeactivatedBanError,
)
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import CheckChatInviteRequest, ImportChatInviteRequest
from telethon.tl.types import ChatInviteAlready

from apps.telegram_bot.tasks import send_message_to_user

from .get_user_with_online_delta import get_user_with_online_delta


def pars(
    order,
    account,
    loop=None,
):
    order.refresh_from_db()
    if not order.in_progress:
        print("[+] Order has stopped")
        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "Заказ завершён",
            )
        return

    order.telethon_accounts.add(account)
    account.is_busy = True
    account.save()

    api_id = account.api_id
    api_hash = account.api_hash
    phone_number = account.phone_number

    client = TelegramClient(
        "telethon_sessions/" + str(phone_number),
        api_id,
        api_hash,
        loop=loop,
    )

    try:
        client.connect()

    except:
        traceback.print_exc()
        client.disconnect()
        account.is_busy = False
        account.is_active = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = (
            "Произошла непредвиденная ошибка при инвайте"
        )
        account.save()

        print("cannot pars channel")
        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)

        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "Произошла непредвиденная ошибка во время парсинга",
            )
        return

    try:
        chat = client.get_entity(order.donor_chat_link)
        client(JoinChannelRequest(chat))
    except ChannelPrivateError:
        client.disconnect()
        print("account has been banned in this channel")
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = "Аккаунт был забанен в этом канале"
        account.save()
        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                f"Аккаунт {phone_number} был забанен в этом канале, перезапускаем с другим аккаунтом",
            )
        return
    except UserDeactivatedBanError:
        client.disconnect()
        print("account has been banned")
        account.is_active = False
        account.is_busy = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = "Аккаунт был забанен навсегда"
        account.save()
        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                f"Аккаунт {phone_number} был забанен навсегда, перезапускаем с другим аккаунтом",
            )
        return
    except ValueError:
        try:
            if isinstance(
                check_invite := client(CheckChatInviteRequest(order.donor_chat_link)),
                ChatInviteAlready,
            ):
                chat = check_invite.chat
            else:
                updates = client(ImportChatInviteRequest(order.donor_chat_link))
                chat = updates.chats[0]
        except ChannelPrivateError:
            client.disconnect()
            print("account has been banned in this channel")
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Аккаунт был забанен в этом канале"
            account.save()
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунт {phone_number} был забанен в этом канале, перезапускаем с другим аккаунтом",
                )
            return
        except InviteHashExpiredError:
            print("Недействительная ссылка на донор группу")

            order.in_progress = False
            order.save()
            order.telethon_accounts.update(is_busy=False)

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
            traceback.print_exc()
            client.disconnect()
            account.is_busy = False
            account.is_active = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = (
                "Произошла непредвиденная ошибка при инвайте"
            )
            account.save()
            print("cannot pars channel")
            order.in_progress = False
            order.save()
            order.telethon_accounts.update(is_busy=False)

            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    "Произошла непредвиденная ошибка во время парсинга",
                )
            return
    except:
        traceback.print_exc()
        client.disconnect()
        account.is_busy = False
        account.is_active = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = (
            "Произошла непредвиденная ошибка при инвайте"
        )
        account.save()
        print("cannot pars channel")
        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)

        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "Произошла непредвиденная ошибка во время парсинга",
            )
        return

    all_participants = []

    try:
        all_participants = client.get_participants(chat, aggressive=False)
    except TypeError:
        try:
            all_participants = client.get_participants(chat, aggressive=True)
        except MultiError:
            client.disconnect()
            print("cannot pars channel")
            account.is_active = False
            account.is_busy = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = "Не получилось спарсить канал"
            account.save()
            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    f"Аккаунту {phone_number} не удалось спарсить канал, перезапускаем с другим аккаунтом",
                )
            return
        except:
            traceback.print_exc()
            client.disconnect()
            account.is_busy = False
            account.is_active = False
            account.date_of_last_deactivate = datetime.datetime.now()
            account.reason_of_last_deactivate = (
                "Произошла непредвиденная ошибка при инвайте"
            )
            account.save()
            print("cannot pars channel")
            order.in_progress = False
            order.save()
            order.telethon_accounts.update(is_busy=False)

            if order.user:
                send_message_to_user.delay(
                    settings.TELEGRAM_MANUAL_BOT_TOKEN,
                    order.user.telegram_id,
                    "Произошла непредвиденная ошибка во время парсинга",
                )
            return
    except:
        traceback.print_exc()
        client.disconnect()
        account.is_busy = False
        account.is_active = False
        account.date_of_last_deactivate = datetime.datetime.now()
        account.reason_of_last_deactivate = (
            "Произошла непредвиденная ошибка при инвайте"
        )
        account.save()
        print("cannot pars channel")
        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)

        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "Произошла непредвиденная ошибка во время парсинга",
            )
        return

    if not chat:
        print("cant pars this chat")

        order.in_progress = False
        order.save()
        order.telethon_accounts.update(is_busy=False)
        client.disconnect()

        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "Не получилось спарсить данный чат вашими аккаунтами",
            )
        return

    client.disconnect()

    with open(
        "pars_results/" + f"{account.api_id}{chat.id}{order.id}.csv",
        "w+",
        encoding="UTF-8",
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
            if order.was_online_user_delta:
                user = get_user_with_online_delta(
                    user=user,
                    was_online_user_delta=order.was_online_user_delta,
                    get_recently_online_users=order.get_recently_online_users,
                )
                if not user:
                    continue

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

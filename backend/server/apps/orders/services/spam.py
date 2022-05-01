#!/usr/bin/env python3
import configparser
import csv
import datetime
import os
import random
import sys
import time
import traceback

from django.conf import settings

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import (
    PeerFloodError,
    FloodWaitError, 
    InputUserDeactivatedError,
)

from apps.orders.services.pars import pars
from apps.telegram_bot.tasks import send_message_to_user
from apps.telethon_app.models import TelethonAccount

from .get_account import get_account
from .get_or_create_eventloop import get_or_create_eventloop


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"




def spam(order):
  

    loop = get_or_create_eventloop()
    account = get_account(order)

    if not account:
        print("you dont have any active accounts")
        order.in_progress = False
        order.save()
        if order.user:
            send_message_to_user.delay(
                settings.TELEGRAM_MANUAL_BOT_TOKEN,
                order.user.telegram_id,
                "У вас не осталось активных аккаунтов, заказ завершён",
            )
        return

    input_file = pars(order, account=account, loop=loop)

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
        return spam(order)

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
        spam(order)
        return

    print(f"Start with {phone_number} account")

    if order.user:
      send_message_to_user.delay(
          settings.TELEGRAM_MANUAL_BOT_TOKEN,
          order.user.telegram_id,
          f"Успешно стартанула рассылка с аккаунта {phone_number}",
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
        if str(user["id"]) in order.affected_users:
            print(gr + "[+] This user already has been affected")
            continue
        order.affected_users.append(user["id"])
        order.save()
        
        SLEEP_TIME = random.randint(9, 24)
        receiver = InputPeerUser(user['id'],user['access_hash'])

        try:
            print(gr+"[+] Sending Message to:", user['name'])
            client.send_message(receiver, order.spam_message)
            print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
            time.sleep(SLEEP_TIME)

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
                    f"Аккаунт {phone_number} временно заблокирован, перезапускаем спам на другом аккаунте",
                )
            spam(order)
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
                    f"Аккаунт {phone_number} временно заблокирован, перезапускаем рассылку на другом аккаунте",
                )
                spam(order)
                return

        except InputUserDeactivatedError:
            print(
                re
                + f"The specified user {user['name']} was deleted"
            )
            continue

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
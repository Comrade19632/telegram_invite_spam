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
from telethon.errors.rpcerrorlist import PeerFloodError

from apps.orders.services.pars import pars
from apps.telegram_bot.tasks import send_message_to_user
from apps.telethon_app.models import TelethonAccount

from .get_or_create_eventloop import get_or_create_eventloop


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

SLEEP_TIME = 10


def spam(order):
    order.in_progress = True
    order.save()

    loop = get_or_create_eventloop()

    input_file = pars(
        target_chat_link=order.donor_chat_link, user_account=order.user, loop=loop
    )

    if not input_file:
        order.in_progress = False
        order.save()
        return

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
                "У вас не осталось активных аккаунтов, заказ завершён",
            )
        return

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
      receiver = InputPeerUser(user['id'],user['access_hash'])
      try:
          print(gr+"[+] Sending Message to:", user['name'])
          client.send_message(receiver, order.message.format(user['name']))
          print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
          time.sleep(SLEEP_TIME)
      except PeerFloodError:
          print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
          client.disconnect()
          sys.exit()
      except Exception as e:
          print(re+"[!] Error:", e)
          print(re+"[!] Trying to continue...")
          continue
      client.disconnect()
      print("Done. Message sent to all users.")
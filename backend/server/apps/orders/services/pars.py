import configparser
import csv
import os
import sys
import time

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from apps.orders.constants import PARS_RESULTS_FOLDER, TELETHON_SESSIONS_FOLDER
from apps.orders.models import TelethonAccount


def pars(target_chat_link, user=None):
    if user:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, owner=user
        ).first()
    else:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True
        ).first()
    if not account:
        return
    api_id = account.api_id
    api_hash = account.api_hash
    phone_number = account.phone_number

    client = TelegramClient(
        TELETHON_SESSIONS_FOLDER + str(phone_number), api_id, api_hash
    )

    try:
        client.connect()
        chat = client.get_entity(target_chat_link)

        client(JoinChannelRequest(chat))

        all_participants = []
        all_participants = client.get_participants(chat, aggressive=False)

        client.disconnect()
    except:
        account.is_active = False
        account.save()
        pars(target_chat_link, user)

    with open(
        PARS_RESULTS_FOLDER + f"{account.api_id}{chat.id}.csv", "w+", encoding="UTF-8"
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
        return f.name

#!/usr/bin/env python3
import configparser
import csv
import os
import random
import sys
import time
import traceback

from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChannel, InputPeerEmpty, InputPeerUser

from apps.orders.constants import TELETHON_SESSIONS_FOLDER
from apps.orders.models import TelethonAccount
from apps.orders.services import pars


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


def invite(target_chat_link, donor_chat_link, user=None):
    input_file = pars(target_chat_link=donor_chat_link, user=user)

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

    client.connect()

    chat = client.get_entity(target_chat_link)

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
        try:
            user_to_add = InputPeerUser(user["id"], user["access_hash"])
            client(InviteToChannelRequest(chat, [user_to_add]))
            print(gr + "[+] Waiting for 10-30 Seconds...")
            time.sleep(random.randrange(10, 30))
        except PeerFloodError:
            print(
                re
                + "[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time."
            )
            invite(target_chat_link, donor_chat_link, user)
        except UserPrivacyRestrictedError:
            print(
                re
                + "[!] The user's privacy settings do not allow you to do this. Skipping."
            )
            continue
        except:
            traceback.print_exc()
            print(re + "[!] Unexpected Error")
            continue

#!/usr/bin/env python3
import configparser
import csv
import os
import random
import sys
import time
import traceback

from telethon.errors.rpcerrorlist import (
    ChatWriteForbiddenError,
    FloodWaitError,
    PeerFloodError,
    UserKickedError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
)
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChannel, InputPeerEmpty, InputPeerUser

from apps.orders.constants import TELETHON_SESSIONS_FOLDER
from apps.orders.models import TelethonAccount
from apps.orders.services.pars import pars


re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


def invite(order):
    input_file = pars(target_chat_link=order.donor_chat_link, user_account=order.user)

    if order.user:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, owner=order.user
        ).first()
    else:
        account = TelethonAccount.objects.filter(
            is_initialized=True, is_active=True
        ).first()
    if not account:
        print("you dont have any active accounts")
        return

    api_id = account.api_id
    api_hash = account.api_hash
    phone_number = account.phone_number

    client = TelegramClient(
        TELETHON_SESSIONS_FOLDER + str(phone_number), api_id, api_hash
    )

    try:
        client.connect()

    except:
        client.disconnect()
        traceback.print_exc()
        account.is_active = False
        account.save()
        invite(order)
        return

    chat = client.get_entity(order.target_chat_link)
    client(JoinChannelRequest(chat))

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
        try:
            user_to_add = InputPeerUser(user["id"], user["access_hash"])
            client(InviteToChannelRequest(chat, [user_to_add]))
            print(gr + "[+] Waiting for 10-30 Seconds...")
            time.sleep(random.randrange(10, 30))
        except FloodWaitError:
            client.disconnect()
            account.is_active = False
            account.save()
            print(
                re
                + "[!] Getting Flood Error from telegram. \n[!] Rerun function with another account"
            )
            invite(order)
            return
        except PeerFloodError:
            client.disconnect()
            account.is_active = False
            account.save()
            print(
                re
                + "[!] Getting Flood Error from telegram. \n[!] Rerun function with another account"
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
        except ChatWriteForbiddenError:
            client.disconnect()
            account.is_active = False
            account.save()
            print(re + "[!] Account can`t write in this chat")
            invite(order)
            return
        except:
            client.disconnect()
            account.is_active = False
            account.save()
            traceback.print_exc()
            print(re + "[!] Unexpected Error")
            invite(order)
            return

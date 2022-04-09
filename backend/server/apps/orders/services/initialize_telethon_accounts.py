from telethon import TelegramClient, connection, events, sync

from apps.orders.constants import TELETHON_FOLDER_SESSION
from apps.orders.models import TelethonAccount


def initialize_telethon_accounts(queryset=None):
    if not queryset:
        queryset = TelethonAccount.objects.filter(is_initialized=True)
    for account in queryset:
        api_id = account.api_id
        api_hash = account.api_hash
        phone_number = account.phone_number

        client = TelegramClient(
            TELETHON_FOLDER_SESSION + str(phone_number), api_id, api_hash
        )
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            try:
                client.sign_in(
                    phone_number, input(f"[{phone_number}] Enter the code: ")
                )
            except:
                print(f"\033[93mНе удалось войти в аккаунт {phone_number}\033[0m")
                continue
        if client.is_user_authorized():
            account.is_initialized = True
            account.save()
        client.disconnect()

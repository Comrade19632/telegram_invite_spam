from tabnanny import check
from telethon import TelegramClient, connection, events, sync

from apps.orders.constants import TELETHON_SESSIONS_FOLDER
from apps.orders.models import TelethonAccount
import time

CHECK_CODE = None
def get_code(verification_code):
    global CHECK_CODE
    CHECK_CODE = verification_code
    print(f'verification_code: {CHECK_CODE}')

def initialize_telethon_accounts(queryset=None):
    if not queryset:
        queryset = TelethonAccount.objects.filter(is_initialized=False, is_active=True)
    for account in queryset:
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
            account.is_active = False
            account.save()
            initialize_telethon_accounts(queryset)

        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            while CHECK_CODE is None:
                time.sleep(3)
            try:
                client.sign_in(phone_number, CHECK_CODE)
                # client.sign_in(
                #     phone_number, input(f"[{phone_number}] Enter the code: ")
                # )
            except:
                client.disconnect()
                print(f"\033[93mНе удалось войти в аккаунт {phone_number}\033[0m")
                continue
        if client.is_user_authorized():
            account.is_initialized = True
            account.save()
        client.disconnect()

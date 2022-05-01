from apps.telethon_app.models import TelethonAccount


def get_account(order):
    accounts = (
        TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, is_busy=False, owner=order.user
        )
        if order.user
        else TelethonAccount.objects.filter(
            is_initialized=True, is_active=True, is_busy=False
        )
    )
    if not accounts:
        return
    for account in accounts:
        if active_related_orders := account.orders_spam.filter(in_progress=True):
            if order in active_related_orders and len(active_related_orders) == 1:
                return account
            else:
                continue
        elif active_related_orders := account.invite_orders.filter(in_progress=True):
            if order in active_related_orders and len(active_related_orders) == 1:
                return account
            else:
                continue
        else:
            return account
    return

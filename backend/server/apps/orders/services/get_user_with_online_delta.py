from telethon.tl.types import UserStatusOffline, UserStatusOnline, UserStatusRecently


def get_user_with_online_delta(user, was_online_user_delta, get_recently_online_users):
    if isinstance(user.status, UserStatusOnline):
        return user
    elif isinstance(user.status, UserStatusRecently):
        if get_recently_online_users:
            return user
    elif isinstance(user.status, UserStatusOffline):
        if was_online_user_delta < user.status.was_online:
            return user
    else:
        return

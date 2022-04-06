from telegram.ext import ConversationHandler


# Определение состояния для диалогов базового меню
(
    SELECTING_MENU,
    PROMOTION_BY_INVITATION,
    PROMOTION_BY_SPAMMING,
    SELECT_INVITE,
    SELECT_SPAMMING,
) = map(chr, range(5))

# Метасостояния
SHOWING, STOPPING, START_OVER = map(chr, range(5, 8))

# Определение состония для определения шагов диалога
(
    CURRENT_MENU,
    INVITE,
    SPAMMING,
    USER_ACTIVITY,
    SHOW_DATA,
    SPAM_CREATIVE,
    ENTER_DONOR_GROUPS,
    CONFIRM,
    ADD_DATA,
) = map(chr, range(8, 17))

# Состояние завершения диалогов
END = ConversationHandler.END

# Дни активности
TWO, FOUR, SIX, EIGHT = 2, 4, 6, 8

# Определение состояния для временного хранения данных
class State:
    invite = {
        "group": "",
        "groups": "",
        "days": "",
    }
    spamming = {
        "group": "",
        "groups": "",
        "days": "",
        "creative": "",
    }

from telegram.ext import CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

from apps.telegram_bot.services.menu_handlers import (
    enter_donor_groups,
    enter_spam_creative,
    enter_target_group,
    enter_user_activity,
    show_data,
)
from apps.telegram_bot.services.step_variables import (
    ADD_DATA,
    EIGHT,
    ENTER_DONOR_GROUPS,
    FOUR,
    SELECTING_MENU,
    SHOW_DATA,
    SIX,
    SPAM_CREATIVE,
    STOPPING,
    TWO,
    USER_ACTIVITY,
)


conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(enter_target_group, pattern="^" + str(ADD_DATA) + "$")
    ],
    states={
        USER_ACTIVITY: [MessageHandler(Filters.text, enter_user_activity)],
        ENTER_DONOR_GROUPS: [MessageHandler(Filters.text, enter_donor_groups)],
        SPAM_CREATIVE: [
            CallbackQueryHandler(
                enter_spam_creative,
                pattern="^"
                + str(TWO)
                + "$|^"
                + str(FOUR)
                + "$|^"
                + str(SIX)
                + "$|^"
                + str(EIGHT)
                + "$",
            )
        ],
        SHOW_DATA: [
            CallbackQueryHandler(
                show_data,
                pattern="^"
                + str(TWO)
                + "$|^"
                + str(FOUR)
                + "$|^"
                + str(SIX)
                + "$|^"
                + str(EIGHT)
                + "$",
            ),
            MessageHandler(Filters.text, show_data),
        ],
    },
    fallbacks=[],
    map_to_parent={
        # Возвращение в базовое меню
        SELECTING_MENU: SELECTING_MENU,
        # Полностью завершить разговор
        STOPPING: STOPPING,
    },
)

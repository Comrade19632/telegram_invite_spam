from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

from apps.telegram_bot.services.menu_handlers import (
    end,
    promotion_with_invitations,
    promotion_with_spamming,
    start,
    stop,
)
from apps.telegram_bot.services.step_variables import (
    CONFIRM,
    END,
    PROMOTION_BY_INVITATION,
    PROMOTION_BY_SPAMMING,
    SELECT_INVITE,
    SELECT_SPAMMING,
    SELECTING_MENU,
    SHOWING,
    STOPPING,
)

from .conv_handler import conv_handler


selection_handlers = [
    CallbackQueryHandler(
        promotion_with_invitations, pattern="^" + str(SELECT_INVITE) + "$"
    ),
    CallbackQueryHandler(
        promotion_with_spamming, pattern="^" + str(SELECT_SPAMMING) + "$"
    ),
    CallbackQueryHandler(start, pattern="^" + str(CONFIRM) + "$"),
    CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
]


def get_menu_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STOPPING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            PROMOTION_BY_INVITATION: [conv_handler],
            PROMOTION_BY_SPAMMING: [conv_handler],
            SELECTING_MENU: selection_handlers,
        },
        fallbacks=[
            CallbackQueryHandler(start, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop),
        ],
    )

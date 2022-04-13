from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, Filters

from apps.telegram_bot.conversation.handlers.telegram_manual_bot import (
    start,
    enter_id,
    enter_hash_id,
    enter_phone_number,
    data_validation,
    verification_code,
    code_check,
    next_conv_menu,
)

from apps.telegram_bot.conversation.step_variables import (
    CONFIRM,
    ENTER_ID,
    ENTER_HASH_ID,
    ENTER_PHONE_NUMBER,
    RESULT_OF_VALIDATION,
    SELECTING_ACTION,
    CHANGE,
    DATA_VALIDATION,
    CHECK_PASS,
    START_PROMO,
    ADD_TG_ACC,
    NEXT_CONV,
)
from apps.telegram_bot.conversation.handlers.common import stop
from apps.telegram_bot.conversation.conversation_handlers.telegram_bot import promotion_conv_menu




def enter_tg_data_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ENTER_ID: [CallbackQueryHandler(enter_id, pattern="^" + str(ENTER_ID) + "$")],
            ENTER_HASH_ID: [MessageHandler(Filters.text, enter_hash_id)],
            ENTER_PHONE_NUMBER: [MessageHandler(Filters.text, enter_phone_number)],
            DATA_VALIDATION: [MessageHandler(Filters.text, data_validation)],
            RESULT_OF_VALIDATION: [
                CallbackQueryHandler(start, pattern="^" + str(CHANGE) + "$"),
                CallbackQueryHandler(verification_code, pattern="^" + str(CONFIRM) + "$"),
            ],
            CHECK_PASS: [MessageHandler(Filters.text, code_check)],
            SELECTING_ACTION: [
                CallbackQueryHandler(next_conv_menu, pattern="^" + str(START_PROMO) + "$"),
                CallbackQueryHandler(start, pattern="^" + str(ADD_TG_ACC) + "$"),
            ],
            NEXT_CONV: [promotion_conv_menu],
        },
        fallbacks=[
            CommandHandler("stop", stop),
        ],
    )

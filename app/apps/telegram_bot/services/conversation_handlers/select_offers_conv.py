from django.conf import settings

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from apps.customers.models import Customer
from apps.offers.models import Offer


SUM, DAYS = range(2)
BUTTONS_ROW_LENGTH = 4


def select_offers(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Введите сумму займа. Например: 30000",
    )
    telegram_chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    telegram_user_name = update.message.chat.username

    Customer.objects.get_or_create(
        telegram_chat_id=telegram_chat_id,
        defaults={"first_name": first_name, "telegram_user_name": telegram_user_name},
    )

    return SUM


def input_sum(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data["sum"] = text

    update.message.reply_text(
        "Введите желаемый срок возврата (дней). Например: 30",
    )

    return DAYS


def input_days(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data["days"] = text

    try:
        offers = Offer.objects.filter(
            is_active=True,
            sum__gte=int(context.user_data["sum"]),
            days__gte=int(context.user_data["days"]),
        )
    except ValueError as error:
        offers = []
        print(error)

    if not offers:
        update.message.reply_text(
            "Не удалось подобрать предложение под ваши запросы, "
            "возможно вы неправильно указали данные. Мы выведем вам все наши актуальные предложения."
        )
        send_offers(update, Offer.objects.filter(is_active=True))

        return ConversationHandler.END

    send_offers(update, offers)

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text(
        "Вы отменили выбор займа", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def get_select_offers_conv_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~Filters.command, select_offers)],
        states={
            SUM: [MessageHandler(Filters.text, input_sum)],
            DAYS: [
                MessageHandler(Filters.text, input_days),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


def send_offers(update, offers):
    for offer in offers:
        caption = f"""
        ✅*{offer.title}*
        ⏳ до {offer.days}дн.
        💰 до {offer.sum}р.
        ⏰ Рассмотрение: {offer.time} мин.
        💬 {offer.feature}
            """
        update.message.reply_photo(
            photo=settings.LETSENCRYPT_HOST + offer.logo.url,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Подать заявку",
                            url=f"https://gl.guruleads.ru/click/{settings.WEBMASTER_ID}/{offer.offerId}",
                        )
                    ],
                ]
            ),
        )

        # update.message.reply_text(
        #     caption,
        #     parse_mode=ParseMode.MARKDOWN,
        #     reply_markup=InlineKeyboardMarkup(
        #         [
        #             [
        #                 InlineKeyboardButton(
        #                     text="Подать заявку",
        #                     url=f"https://gl.guruleads.ru/click/{settings.WEBMASTER_ID}/{offer.offerId}",
        #                 )
        #             ],
        #         ]
        #     ),
        # )
        update.message.reply_text(
            "▪▪▪▪▪▪▪▪▪▪▪▪▪",
        )

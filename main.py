from enum import IntEnum
import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters,
)


logger = logging.getLogger("moneybot")


class States(IntEnum):
    Choices = 0
    NewPurchase = 1
    CancelPurchase = 2
    NewPayment = 3
    CancelPayment = 4
    BackToStart = 5


ACTIONS = ["Purchase", "Payment"]


def start(update, context):
    reply_keyboard = [ACTIONS]
    update.message.reply_text(
        "What do you want to do?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False),
    )
    return States.Choices


def do_something(update, context):
    update.message.reply_text("Cool")
    return States.BackToStart


def fallback(update, context):
    update.message.reply_text("I did not understand")
    return States.BackToStart


def main():
    logging.basicConfig(level=logging.DEBUG)
    updater = Updater("359826646:AAEGqZFk0Mlj1Yi0QS0QhkDbgHJQUUiBnn4", use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.Choices: [
                MessageHandler(Filters.text("Purchase"), do_something),
                MessageHandler(Filters.text("Payment"), do_something),
            ],
            States.NewPurchase: [MessageHandler(Filters.regex(r"\d+"), do_something)],
            States.BackToStart: [MessageHandler(Filters.text, start)],
        },
        fallbacks=[fallback],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

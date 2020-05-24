from datetime import datetime
from enum import IntEnum
import logging
import re

from aiogram import Bot, Dispatcher, types, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.files import MemoryStorage
from aiogram.utils import executor

from db import Database

logger = logging.getLogger("moneybot")


class States(StatesGroup):
    choice = State()

    purchase_choice = State()
    purchase = State()
    purchase_list = State()
    awaiting_purchases = State()

    payment_choice = State()
    payment = State()
    payment_amount = State()
    payment_list = State()


purchase_format = r"(\w+)\s+(\d+(?:\.\d{2})?)\s*€?"

with open("TOKEN", "r") as f:
    bot = Bot(f.read().strip())
dp = Dispatcher(bot, storage=MemoryStorage())
database = Database("storage.db")


@dp.message_handler(text="cancel", state="*")
async def cancel(message, state):
    await message.reply("Canceling..")
    await state.finish()


@dp.message_handler(commands="start")
async def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add("Purchase", "Payment")

    await States.choice.set()
    await message.reply("What do you want to do?", reply_markup=markup)


@dp.message_handler(text="Purchase", state=States.choice)
async def purchase(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("List purchases", "New purchase(s)")

    await States.purchase_choice.set()
    await message.reply("What exactly do you want to do?", reply_markup=markup)


@dp.message_handler(text="List purchases", state=States.purchase_choice)
async def list_payments(message, state):
    history = "\n".join(database.payments)
    await message.reply(f"Showing you the last purchases made:\n{history}")
    await state.finish()


@dp.message_handler(text="New purchase(s)", state=States.purchase_choice)
async def awaiting_new_purchases(message, state):
    await States.awaiting_purchases.set()
    await message.reply("What did you purchase? (Type ")


@dp.message_handler(
    regexp=purchase_format, state=States.awaiting_purchases,
)
async def new_purchase(message):
    matches = re.findall(purchase_format, message.text)
    for product, price in matches:
        await message.reply(f"Ah, you bought {product} for {price} €.")


@dp.message_handler(text="Payment", state=States.choice)
async def payment(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("List payments", "New payment")

    await States.payment_choice.set()
    await message.reply("What exactly do you want to do?", reply_markup=markup)


@dp.message_handler(text="List payments", state=States.payment_choice)
async def list_payments(message, state):
    history = "\n".join(database.payments)
    await message.reply(f"Showing you the last payments made:\n{history}")
    await state.finish()


@dp.message_handler(text="New payment", state=States.payment_choice)
async def new_payment(message):
    await States.payment_amount.set()
    await message.reply("How much do you want to pay?")


@dp.message_handler(regexp=r"\d+(\.\d{2})?", state=States.payment_amount)
async def payment_amount(message, state):
    user = message.from_user.mention
    await message.reply(f"{user} wants to pay {message.text}")
    await state.finish()


@dp.message_handler(regexp=".*", state=States.payment_amount)
async def invalid_payment_amount(message):
    await message.reply(f"Input must be a valid amount of money..")
    await States.payment_amount.set()
    await message.reply("How much do you want to pay?")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=True)

from enum import IntEnum
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.files import MemoryStorage
from aiogram.utils import executor

logger = logging.getLogger("moneybot")


class States(StatesGroup):
    purchase = State()
    payment = State()
    payment_amount = State()
    choice = State()


bot = Bot("359826646:AAEGqZFk0Mlj1Yi0QS0QhkDbgHJQUUiBnn4")
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text="cancel", state="*")
async def cancel(message, state):
    await message.reply("Canceling..")
    await state.finish()


@dp.message_handler(commands="start")
async def start(message):
    await States.choice.set()
    await message.reply("What do you want to do?")


@dp.message_handler(
    lambda message: "purchase" in message.text.lower(), state=States.choice
)
async def purchase(message):
    await message.reply("Purchase")


@dp.message_handler(
    lambda message: "payment" in message.text.lower(), state=States.choice
)
async def payment(message):
    await States.payment_amount.set()
    await message.reply("How much do you want to pay?")


@dp.message_handler(regexp=r"\d+(\.\d{2})?", state=States.payment_amount)
async def payment_amount(message):
    await message.reply(f"You want to pay {message.text}")


@dp.message_handler(regexp=".*", state=States.payment_amount)
async def invalid_payment_amount(message):
    await message.reply(f"Invalid")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=True)

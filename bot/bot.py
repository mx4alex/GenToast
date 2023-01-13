from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

import pika
import asyncio
import os

import markups as buttons
import bot_producer
import bot_consumer

import motor
from aiogram.contrib.fsm_storage.mongo import MongoStorage
import pymongo

storage = MongoStorage(host=os.getenv("MONGO_HOST"), port=os.getenv("MONGO_PORT"), db_name='aiogram_fsm')

bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher(bot, storage=storage)

amqp_url = os.getenv("RABBITMQ_URL")
connection_parameters = pika.URLParameters(amqp_url)

class FSMGeneration(StatesGroup):
    input_state = State()
    answer_state = State()

@dp.message_handler(commands=['start'])
async def start(message):    
    await message.answer(f"Здравствуйте, {message.from_user.first_name}👤! \nВыберете📍 команду из предложенного меню🧾", reply_markup=buttons.main_keyboard)

@dp.message_handler(Text(equals="Информация о боте🤖"))
async def info(message: types.Message):
    await message.answer("*GenToast* - бот для генерации🪄 праздничных тостов. \nУправление🕹 ботом производится с помощью меню🧾", parse_mode="Markdown")

@dp.message_handler(Text(equals="Сгенерировать тост🥂"))
async def generation(message: types.Message):
    await FSMGeneration.input_state.set()
    await message.reply("Выберете праздник🎊", reply_markup=buttons.celebration_keyboard)

@dp.message_handler(state=FSMGeneration.input_state)
async def send_predict(message: types.Message, state: FSMContext):   
    bot_producer.publish(message.from_user.id, message.text, connection_parameters)

    await message.reply("Ожидайте, генерация может занять некоторое время⏱", reply_markup=buttons.main_keyboard)
    await state.finish()
    await FSMGeneration.answer_state.set()

@dp.message_handler(state=FSMGeneration.answer_state)
async def wait_answer(message: types.Message, state: FSMContext):
    await message.reply("Дождитесь окончания генерации⏳")
    await state.finish()

@dp.message_handler()
async def error_command(message: types.Message):
    await message.answer(f"Команда '{message.text}' не найдена.\nВыберете📍 команду из предложенного меню🧾")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(bot_consumer.consume(bot, storage, amqp_url))
    executor.start_polling(dp)

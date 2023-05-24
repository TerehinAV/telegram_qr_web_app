#!/usr/bin/env python3
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""

Installation:

    pip install python-telegram-bot --upgrade


Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""

import os
import logging
import asyncio
import aiogram
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

TOKEN = os.environ['TOKEN']
URL = 'https://mboretto.github.io/easy-qr-scan-bot/'
REDIS_HOST = 'localhost'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()
bot = aiogram.Bot(token=TOKEN, loop=loop)

storage = RedisStorage(host=REDIS_HOST, db=5)
dp = Dispatcher(bot, storage=storage)


async def _add_menu_button():
    menu_button = aiogram.types.MenuButtonWebApp(text="Scan QR", web_app=aiogram.types.WebAppInfo(url=URL))
    print(await bot.set_chat_menu_button(menu_button=menu_button))


loop.create_task(_add_menu_button())


@dp.message_handler(chat_type=[aiogram.types.ChatType.PRIVATE], state="*", commands=['scan'])
async def on_start_command(message: aiogram.types.Message):
    """Обработчик на старте бота"""
    keyboard = aiogram.types.InlineKeyboardMarkup()
    keyboard.add(aiogram.types.InlineKeyboardButton('Scan QR', web_app=aiogram.types.WebAppInfo(url=URL)))
    await message.reply("To start scanning press the button:", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=False)


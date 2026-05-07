# Версия для локальной разработки с .env файлом
import asyncio
import logging
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardButton,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Загружаем переменные из .env
load_dotenv()

# ======================================================
# НАСТРОЙКИ
# ======================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8374022888:AAGoZoIoMYPkyAOJy4nYVUPWUUb32Xw5mMY")

FUNPAY_URL = "https://funpay.com/users/17089244/"
CHANNEL_URL = "https://t.me/gift_hub_crypto"
SUPPORT_URL = "https://t.me/muffinn_2"

# Локальная картинка
BANNER_PATH = "banner.jpg"

# ======================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Остальной код из bot.py идентичен...

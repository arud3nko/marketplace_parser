from app.config.config import TOKEN

from aiogram import Bot
from aiogram.enums import ParseMode


bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

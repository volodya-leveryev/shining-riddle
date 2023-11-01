"""Telegram-бот для генерации РПД"""
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import bold

# Константы
TOKEN = getenv("TG_TOKEN")

# Диспетчер сообщений
disp = Dispatcher()


@disp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Команда /start"""
    await message.answer(f"Hello {bold(message.from_user.full_name)}")


async def main() -> None:
    """Запуск бота"""
    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    await disp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())

"""Telegram-бот для генерации РПД"""
import asyncio
import logging
import sys
import tomllib
from collections.abc import Callable, Coroutine
from os.path import join

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, User
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.markdown import bold

# Конфигурация
config_filename = join('data', 'config.toml')
with open(config_filename, mode='rb') as config_file:
    config = tomllib.load(config_file)
    TOKEN = config.get('TG_TOKEN')
    ADMINS = config.get('ADMINS')
    USERS = config.get('USERS')
    URL_CREATE_COURSE = config.get('URL_CREATE_COURSE')

# Диспетчер сообщений
disp = Dispatcher()

# Типы данных
Handler = Callable[[Message], Coroutine[None]]


def user_groups(user: User) -> [str]:
    """Определяем в каких группах состоит пользователь"""
    groups = []
    if {user.id, user.username} & set(USERS):
        groups.append('users')
    if {user.id, user.username} & set(ADMINS):
        groups.append('admins')
    return groups


def auth_user_required(func: Handler) -> Handler:
    """Декоратор для проверки прав пользователя"""
    async def wrapper(message: Message) -> None:
        """Обертка для проверки прав пользователя"""
        groups = user_groups(message.from_user)
        if 'users' in groups or 'admins' in groups:
            # Проверка пройдена успешно
            await func(message)
        else:
            await message.answer("Sorry, I don't know you")
    return wrapper


@disp.message(CommandStart())
@auth_user_required
async def cmd_start(msg: Message) -> None:
    """Команда /start"""
    app = WebAppInfo(url=URL_CREATE_COURSE)
    btn = InlineKeyboardButton(text="test",  web_app=app)
    kbd = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await msg.answer(f"Hello {bold(msg.from_user.full_name)}", reply_markup=kbd)


@disp.message()
async def echo_all(msg: Message) -> None:
    logging.info(msg.text)
    await msg.answer(msg.text)


async def main() -> None:
    """Запуск бота"""
    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    await disp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())

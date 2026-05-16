"""
Простой учебный Telegram-бот на aiogram 3.
Что умеет:
  /start  — приветствует пользователя по имени
  /help   — показывает список команд
  /about  — рассказывает о проекте
  Любой текст — отвечает "Вы написали: ..."
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Берём токен бота из переменной окружения BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "Не найден BOT_TOKEN. Создайте файл .env и укажите в нём BOT_TOKEN=ваш_токен"
    )

# Включаем логирование, чтобы видеть, что происходит с ботом
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Router — это контейнер для хендлеров (обработчиков сообщений) в aiogram 3
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обработчик команды /start — приветствует пользователя по имени."""
    # full_name берёт имя + фамилию пользователя из Telegram
    name = message.from_user.full_name if message.from_user else "друг"
    await message.answer(
        f"Привет, {name}! 👋\n\n"
        "Я простой учебный бот на aiogram 3.\n"
        "Я умею:\n"
        "• отвечать на команды /start, /help, /about\n"
        "• повторять любое текстовое сообщение, которое ты мне пришлёшь\n\n"
        "Напиши /help, чтобы увидеть список команд."
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обработчик команды /help — выводит список доступных команд."""
    await message.answer(
        "📋 Доступные команды:\n\n"
        "/start — начать работу с ботом\n"
        "/help — показать этот список\n"
        "/about — информация о проекте\n\n"
        "А ещё я повторю любое текстовое сообщение, которое ты мне пришлёшь."
    )


@router.message(Command("about"))
async def cmd_about(message: Message) -> None:
    """Обработчик команды /about — рассказывает о проекте."""
    await message.answer(
        "ℹ️ Об этом боте\n\n"
        "Это учебный проект, созданный для знакомства с библиотекой aiogram 3 "
        "и Telegram Bot API.\n"
        "Цель — научиться писать простых ботов на Python: "
        "обрабатывать команды, отвечать на сообщения и работать с переменными окружения."
    )


# F.text — фильтр, который срабатывает на любое сообщение с текстом.
# Команды (/start и т.д.) уже обработаны выше, до этого хендлера они не доходят.
@router.message(F.text)
async def echo_text(message: Message) -> None:
    """Эхо-обработчик: повторяет любой присланный текст."""
    await message.answer(f"Вы написали: {message.text}")


async def main() -> None:
    """Точка входа: создаём бота, подключаем роутер и запускаем поллинг."""
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # start_polling постоянно опрашивает Telegram на наличие новых сообщений
    logging.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Корректно завершаем работу при нажатии Ctrl+C
        logging.info("Бот остановлен.")

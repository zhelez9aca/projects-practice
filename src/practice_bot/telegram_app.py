"""Telegram runtime using aiogram."""

from __future__ import annotations

from practice_bot.config import Settings
from practice_bot.engine import PracticeBotEngine


def _build_keyboard(suggestions: list[str]):
    from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

    rows: list[list[KeyboardButton]] = []
    current_row: list[KeyboardButton] = []

    for label in suggestions:
        current_row.append(KeyboardButton(text=label))
        if len(current_row) == 2:
            rows.append(current_row)
            current_row = []

    if current_row:
        rows.append(current_row)

    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, is_persistent=True)


async def run_bot(settings: Settings) -> None:
    try:
        from aiogram import Bot, Dispatcher
        from aiogram.filters import CommandStart
        from aiogram.types import Message
    except ImportError as exc:
        raise RuntimeError(
            "Для запуска Telegram-бота установите зависимости: "
            "`python3 -m pip install -r requirements.txt`."
        ) from exc

    engine = PracticeBotEngine()
    bot = Bot(token=settings.require_bot_token())
    dispatcher = Dispatcher()

    @dispatcher.message(CommandStart())
    async def on_start(message: Message) -> None:
        reply = engine.respond("/start")
        await message.answer(reply.text, reply_markup=_build_keyboard(reply.suggestions))

    @dispatcher.message()
    async def on_message(message: Message) -> None:
        reply = engine.respond(message.text or "")
        await message.answer(reply.text, reply_markup=_build_keyboard(reply.suggestions))

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()

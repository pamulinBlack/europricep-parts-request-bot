import logging
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# ================= НАСТРОЙКИ =================

BOT_TOKEN = os.getenv("BOT_TOKEN")
MANAGERS_CHAT_ID = -1003773037156  # твой chat_id группы

MANAGER_TELEGRAM_URL = "https://t.me/pamulinblack"
MANAGER_WHATSAPP_URL = "https://wa.me/79614400837"
MANAGER_PHONE = "+7 (999) 3602028"

# =============================================

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- КЛАВИАТУРЫ ----------

after_request_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Оформить ещё одну заявку")],
        [KeyboardButton(text="☎️ Связаться с менеджером")]
    ],
    resize_keyboard=True
)

contact_methods_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Telegram")],
        [KeyboardButton(text="📱 WhatsApp")],
        [KeyboardButton(text="📞 Телефон")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

# ---------- ХЕНДЛЕРЫ ----------

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Вас приветствует служба подбора деталей.\n\n"
        "Для ускорения обработки заявки, укажите, пожалуйста:\n"
        "1. ID клиента / Наименование\n"
        "2. Имя контактного лица\n"
        "3. VIN\n"
        "4. Марка автомобиля\n"
        "5. Наименование детали\n"
        "6. Количество"
    )


@dp.message()
async def handle_message(message: Message):

    # игнорируем любые группы и каналы
    if message.chat.type != "private":
        return

    # оформить ещё одну заявку
    if message.text == "📝 Оформить ещё одну заявку":
        await message.answer(
            "Пожалуйста, укажите данные для новой заявки:\n"
            "1. ID клиента / Наименование\n"
            "2. Имя контактного лица\n"
            "3. VIN\n"
            "4. Марка автомобиля\n"
            "5. Наименование детали\n"
            "6. Количество"
        )
        return

    # связь с менеджером
    if message.text == "☎️ Связаться с менеджером":
        await message.answer(
            "Выберите удобный способ связи с менеджером:",
            reply_markup=contact_methods_keyboard
        )
        return

    # Telegram
    if message.text == "💬 Telegram":
        await message.answer(
            f"Напишите менеджеру в Telegram:\n👉 {MANAGER_TELEGRAM_URL}",
            reply_markup=after_request_keyboard
        )
        return

    # WhatsApp
    if message.text == "📱 WhatsApp":
        await message.answer(
            f"Напишите менеджеру в WhatsApp:\n👉 {MANAGER_WHATSAPP_URL}",
            reply_markup=after_request_keyboard
        )
        return

    # Телефон
    if message.text == "📞 Телефон":
        await message.answer(
            f"Позвоните менеджеру:\n📞 {MANAGER_PHONE}",
            reply_markup=after_request_keyboard
        )
        return

    # Назад
    if message.text == "⬅️ Назад":
        await message.answer(
            "Что вы хотите сделать дальше?",
            reply_markup=after_request_keyboard
        )
        return

    # ---------- ОБРАБОТКА ЗАЯВКИ ----------

    text = (
        "🛠 Новая заявка\n\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {message.from_user.id}\n\n"
        f"📋 Заявка:\n{message.text}"
    )

    await bot.send_message(MANAGERS_CHAT_ID, text)

    await message.answer(
        "Спасибо! Заявка принята.\n"
        "Что вы хотите сделать дальше?",
        reply_markup=after_request_keyboard
    )


# ---------- ЗАПУСК ----------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

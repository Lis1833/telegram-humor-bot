import os
import random
from datetime import datetime

import pytz
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ================== НАСТРОЙКИ ==================

BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"
CHAT_ID = -5084894998

MOSCOW_TZ = pytz.timezone("Europe/Moscow")

BASE_URL = os.environ.get("RAILWAY_STATIC_URL", "https://your-railway-app.up.railway.app")
WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

# ================== ТЕКСТЫ ==================

PHOTO_REPLIES = [
    "📸 Ого, вот это кадр!", "😂 Картинка огонь", "🖼 Такое надо в рамку",
    "👀 Я всё видел", "😄 Чат одобряет", "🔥 Это достойно лайка",
    "🤣 Мемный потенциал", "😏 Подозрительно смешно", "📷 Фотка дня",
    "😂 Сохраняю в память", "🫠 Красиво пошло", "🤌 Эстетика",
    "😎 Хорош", "🤡 Ну ты выдал", "🖌 Искусство",
    "📸 Скрин судьбы", "😂 Улыбнуло", "👁 Вижу, вижу",
    "😆 Зачёт", "🫡 Принято"
]

VIDEO_REPLIES = [
    "🎥 Ну всё, залипли", "😂 Видео решает", "🍿 Попкорн где?",
    "👀 Сейчас будет экшн", "🔥 Норм пошло", "🤣 Это можно пересматривать",
    "🎬 Режиссёр доволен", "😏 Интрига", "🫣 Опасно красиво",
    "😄 Вот это движ", "📹 Камера, мотор!", "😂 Чистый контент",
    "🤯 Неожиданно", "😎 Сильная подача", "🎞 Классика",
    "🤣 Минутка кайфа", "👁 Смотрю внимательно", "🔥 Годно",
    "😆 Хорошо зашло", "🫡 Видео принято"
]

SILENCE_MESSAGES = [
    "🤫 В группе подозрительная тишина…", "😴 Давно не было смешного контента",
    "😂 Чат скучает по мемам", "👀 Такое чувство, что все затаились",
    "🫠 Народ, оживаем", "☕ Все ушли за кофе?"
]

# ================== HANDLERS ==================

async def on_photo(update: Update, context):
    await update.message.reply_text(random.choice(PHOTO_REPLIES))

async def on_video(update: Update, context):
    await update.message.reply_text(random.choice(VIDEO_REPLIES))

# ================== SCHEDULE ==================

async def send_silence(app):
    await app.bot.send_message(CHAT_ID, random.choice(SILENCE_MESSAGES))

async def send_time(app):
    now = datetime.now(MOSCOW_TZ).strftime("%d.%m.%Y %H:%M")
    await app.bot.send_message(CHAT_ID, f"🕒 Сейчас в Москве: {now}")

async def post_init(app):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_silence, "interval", minutes=30, args=[app])
    scheduler.add_job(send_time, "interval", hours=1, args=[app])
    scheduler.start()

    await app.bot.set_webhook(WEBHOOK_URL)

# ================== TELEGRAM APP ==================

telegram_app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .post_init(post_init)
    .build()
)

telegram_app.add_handler(MessageHandler(filters.PHOTO, on_photo))
telegram_app.add_handler(MessageHandler(filters.VIDEO, on_video))

# ================== FLASK ==================

flask_app = Flask(__name__)

@flask_app.post(WEBHOOK_PATH)
async def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"

@flask_app.get("/")
def health():
    return "Bot is running"

# ================== START ==================

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

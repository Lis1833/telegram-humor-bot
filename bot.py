from zoneinfo import ZoneInfo
import random
import asyncio
import os
import sys

# ====== НАСТРОЙКИ ======
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk")
CHAT_ID = int(os.environ.get("CHAT_ID", "-5084894998"))
PORT = 5000

# ====== ФРАЗЫ ======
PHOTO_REPLIES = [
    "📸 Вот это кадр 😄",
    "🖼 Скриншот эпохи",
    "😂 Картинка засчитана",
    "👀 А с этого места подробнее",
    "🔥 Контент подъехал",
    "🫠 Красота требует лайков",
]

VIDEO_REPLIES = [
    "🎬 Попкорн где?",
    "😂 Видео — топ",
    "📹 Сейчас будет интересно",
    "👀 Смотрим всем чатом",
    "🔥 Контент пошёл",
    "🫣 Надеюсь без жести",
]

SILENCE_MESSAGES = [
    "🤫 В чате тишина… где мемы?",
    "😴 Чат уснул? Срочно смешное!",
    "👀 Давненько тут не смеялись",
    "📉 Уровень юмора падает",
    "😂 Срочно нужен мем",
]

# ====== FLASK ======
app = Flask(__name__)

telegram_app = None

def init_telegram_app():
    global telegram_app
    if not BOT_TOKEN:
        return None
    
    telegram_app = Application.builder().token(BOT_TOKEN).build()
    
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ Бот запущен и работает")

    async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if random.random() < 0.5:
            await update.message.reply_text(random.choice(PHOTO_REPLIES))

    async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if random.random() < 0.5:
            await update.message.reply_text(random.choice(VIDEO_REPLIES))

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    telegram_app.add_handler(MessageHandler(filters.VIDEO, on_video))

    async def silence_job(context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=random.choice(SILENCE_MESSAGES),
        )

    async def time_job(context: ContextTypes.DEFAULT_TYPE):
        now = datetime.now(ZoneInfo("Europe/Moscow"))
        text = now.strftime("🕒 %d.%m.%Y — %H:%M (МСК)")
        await context.bot.send_message(chat_id=CHAT_ID, text=text)

    telegram_app.job_queue.run_repeating(silence_job, interval=1800, first=1800)
    telegram_app.job_queue.run_repeating(time_job, interval=3600, first=3600)
    
    return telegram_app

# ====== WEBHOOK ======
@app.route("/webhook", methods=["POST"])
def webhook():
    if telegram_app is None:
        return "Bot not configured - missing BOT_TOKEN", 503
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "ok"

@app.route("/")
def index():
    if BOT_TOKEN:
        return "Bot is running"
    else:
        return "Bot is not configured. Please set the BOT_TOKEN environment variable."

# ====== START ======
if __name__ == "__main__":
    if BOT_TOKEN:
        init_telegram_app()
        print("Telegram bot initialized successfully")
    else:
        print("WARNING: BOT_TOKEN not set. Set it in Secrets to enable Telegram functionality.")
    app.run(host="0.0.0.0", port=PORT)
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from datetime import datetime
from zoneinfo import ZoneInfo
import random
import asyncio

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"
CHAT_ID = -5084894998
PORT = 8080

# ====== ФРАЗЫ ======
PHOTO_REPLIES = [
    "📸 Вот это кадр 😄",
    "🖼 Скриншот эпохи",
    "😂 Картинка засчитана",
    "👀 А с этого места подробнее",
    "🔥 Контент подъехал",
    "🫠 Красота требует лайков",
]

VIDEO_REPLIES = [
    "🎬 Попкорн где?",
    "😂 Видео — топ",
    "📹 Сейчас будет интересно",
    "👀 Смотрим всем чатом",
    "🔥 Контент пошёл",
    "🫣 Надеюсь без жести",
]

SILENCE_MESSAGES = [
    "🤫 В чате тишина… где мемы?",
    "😴 Чат уснул? Срочно смешное!",
    "👀 Давненько тут не смеялись",
    "📉 Уровень юмора падает",
    "😂 Срочно нужен мем",
]

# ====== FLASK ======
app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()

# ====== HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот запущен и работает")

async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5:
        await update.message.reply_text(random.choice(PHOTO_REPLIES))

async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5:
        await update.message.reply_text(random.choice(VIDEO_REPLIES))

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.PHOTO, on_photo))
telegram_app.add_handler(MessageHandler(filters.VIDEO, on_video))

# ====== JOBS ======
async def silence_job(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=random.choice(SILENCE_MESSAGES),
    )

async def time_job(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(ZoneInfo("Europe/Moscow"))
    text = now.strftime("🕒 %d.%m.%Y — %H:%M (МСК)")
    await context.bot.send_message(chat_id=CHAT_ID, text=text)

telegram_app.job_queue.run_repeating(silence_job, interval=1800, first=1800)
telegram_app.job_queue.run_repeating(time_job, interval=3600, first=3600)

# ====== WEBHOOK ======
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return "ok"

@app.route("/")
def index():
    return "Bot is running"

# ====== START ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

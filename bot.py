import random
import datetime
import feedparser
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import nest_asyncio
import asyncio

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"
CHAT_ID = -5084894998
PORT = int(os.environ.get("PORT", 5000))
WEBHOOK_URL = "https://your-service-name.onrender.com/telegram"  # Заменить на реальный URL сервиса

# ===== ЮМОРНЫЕ ФРАЗЫ =====
PHOTO_REPLIES = [
    "🖼 Так… это искусство или мем?",
    "😂 Картинка сказала больше, чем слова",
    "👀 А вот с этого места поподробнее",
]

VIDEO_REPLIES = [
    "🎬 Попкорн где?",
    "😂 Видео — лучший аргумент",
    "🫣 Это точно можно смотреть?",
]

JOKES = [
    "Почему программисты путают Хэллоуин и Рождество? OCT 31 = DEC 25 😄",
    "Баг — это фича, о которой ты ещё не знаешь 😉",
    "Сначала был кофе, потом код ☕💻",
]

SUBREDDITS_RSS = [
    "https://www.reddit.com/r/memes/.rss",
    "https://www.reddit.com/r/ProgrammerHumor/.rss",
]

# ===== АНТИФЛУД =====
LAST_REPLY = 0
COOLDOWN = 120  # секунд между ответами

# ===== ФУНКЦИИ =====
def can_reply():
    global LAST_REPLY
    import time
    now = time.time()
    if now - LAST_REPLY > COOLDOWN:
        LAST_REPLY = now
        return True
    return False

def get_meme():
    try:
        feed = feedparser.parse(random.choice(SUBREDDITS_RSS))
        if feed.entries:
            return random.choice(feed.entries).link
    except Exception:
        return None
    return None

# ===== ОБРАБОТЧИКИ =====
async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and can_reply():
        await update.message.reply_text(random.choice(PHOTO_REPLIES))

async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and can_reply():
        await update.message.reply_text(random.choice(VIDEO_REPLIES))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен через Webhook! 🟢")

# ===== ЧАСОВОЕ СООБЩЕНИЕ =====
async def hourly_job(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().strftime("%H:%M")
    await context.bot.send_message(CHAT_ID, f"⏰ Текущее время: {now}")

    if random.choice([True, False]):
        meme = get_meme()
        if meme:
            await context.bot.send_message(CHAT_ID, f"😂 Мем дня:\n{meme}")
    else:
        await context.bot.send_message(CHAT_ID, random.choice(JOKES))

# ===== ОСНОВНАЯ ФУНКЦИЯ =====
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Хендлеры
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.VIDEO, on_video))

    # Планировщик APScheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(hourly_job, "interval", hours=1, args=[app.bot])
    scheduler.start()

    # Запуск Webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

# ===== ЗАПУСК =====
if __name__ == "__main__":
    nest_asyncio.apply()  # позволяет re-enter в уже существующий loop Render
    asyncio.get_event_loop().run_until_complete(main())

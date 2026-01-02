import random
import time
import feedparser
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import nest_asyncio

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"
CHAT_ID = -5084894998

# ===== ЮМОР =====
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

LAST_REPLY = 0
COOLDOWN = 120

# ===== ФУНКЦИИ =====
def can_reply():
    global LAST_REPLY
    now = time.time()
    if now - LAST_REPLY > COOLDOWN:
        LAST_REPLY = now
        return True
    return False

def get_meme():
    feed = feedparser.parse(random.choice(SUBREDDITS_RSS))
    if feed.entries:
        return random.choice(feed.entries).link
    return None

async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and can_reply():
        await update.message.reply_text(random.choice(PHOTO_REPLIES))

async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and can_reply():
        await update.message.reply_text(random.choice(VIDEO_REPLIES))

async def hourly_job(context: ContextTypes.DEFAULT_TYPE):
    if random.choice([True, False]):
        meme = get_meme()
        if meme:
            await context.bot.send_message(CHAT_ID, f"😂 Мем дня:\n{meme}")
    else:
        await context.bot.send_message(CHAT_ID, random.choice(JOKES))

# ===== ОСНОВНАЯ ФУНКЦИЯ =====
async def main():
    nest_asyncio.apply()  # нужно для Render
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ===== Добавляем обработчики =====
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.VIDEO, on_video))

    # ===== Планировщик =====
    scheduler = AsyncIOScheduler()

    async def start_scheduler():
        scheduler.add_job(hourly_job, "interval", hours=1, args=[app.bot])
        scheduler.start()

    # ===== Инициализация приложения =====
    await app.initialize()  

    # ===== Запуск планировщика в уже существующем loop =====
    app.create_task(start_scheduler())

    # ===== Запуск polling =====
    await app.run_polling()

# ===== ЗАПУСК на Render =====
if __name__ == "__main__":
    asyncio.run(main())

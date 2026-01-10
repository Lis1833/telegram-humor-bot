import os
import asyncio
import random
import time
from datetime import datetime, timezone, timedelta

import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ===== Переменные из GitHub Secrets =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# ===== Реакции на фото =====
PHOTO_REPLIES = [
    "🖼 Так… это искусство или мем?",
    "📸 Скриншот судьбы принят 😄",
    "🖌 Вот это поворот!",
    "👀 А вот с этого места поподробнее",
    "😂 Картинка сказала больше, чем слова",
    "🫠 Чат официально стал красивее",
    "🤔 Не уверен, что понимаю...",
    "😎 Картинка для вдохновения",
    "🔥 Это точно огонь!",
    "👏 Отличная работа!",
    "😳 Вот это да!",
    "🤣 Хохот до слёз",
    "🙃 Переворачиваем всё с ног на голову",
    "💡 Интересная идея",
    "😏 С намёком на юмор",
    "😮 Вау, неожиданно",
    "🫡 Заслуживает лайка",
    "🫢 Неожиданно мило",
    "😂 Чистый мем",
    "😬 Ну такое…"
]

# ===== Реакции на видео =====
VIDEO_REPLIES = [
    "🎬 Попкорн где?",
    "📹 Ну всё, залипли",
    "👀 Сейчас будет что-то интересное",
    "😂 Видео — лучший аргумент",
    "🎞 Надеюсь, без сюжета как в артхаусе",
    "🫣 Это точно можно смотреть?",
    "😎 Видеоконтент на максималках",
    "🔥 Горячий ролик!",
    "👏 Браво!",
    "🤣 Смех в кадре",
    "🙃 Улыбка гарантирована",
    "💡 Креатив на высоте",
    "😏 С намёком на юмор",
    "😮 Шокирующая сцена",
    "🫡 Заслуживает аплодисментов",
    "🫢 Сюрприз!",
    "😂 Чистый юмор",
    "😬 Неловкий момент",
    "🤯 Мозг взорван",
    "😅 Вот это да!"
]

# ===== Список шуток =====
JOKES_LIST = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 = DEC 25 😄",
    "Баг — это фича, о которой ты ещё не знаешь 😉",
    "Учёные доказали: кофе — источник счастья ☕",
    "Сначала был кофе, потом код ☕💻"
]

# ===== RSS мемов =====
SUBREDDITS_RSS = [
    "https://www.reddit.com/r/memes/.rss",
    "https://www.reddit.com/r/dankmemes/.rss",
    "https://www.reddit.com/r/ProgrammerHumor/.rss"
]

# ===== Антифлуд =====
LAST_REPLY_TIME = 0
COOLDOWN = 120  # секунд между реакциями

# ===== Функции =====
def get_rss_meme():
    try:
        subreddit_rss = random.choice(SUBREDDITS_RSS)
        feed = feedparser.parse(subreddit_rss)
        posts = feed.entries
        if not posts:
            return None
        post = random.choice(posts)
        return post.link
    except Exception:
        return None

async def can_reply():
    global LAST_REPLY_TIME
    now = time.time()
    if now - LAST_REPLY_TIME > COOLDOWN:
        LAST_REPLY_TIME = now
        return True
    return False

# ===== Обработчики медиа =====
async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and await can_reply():
        await update.message.reply_text(random.choice(PHOTO_REPLIES))

async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and await can_reply():
        await update.message.reply_text(random.choice(VIDEO_REPLIES))

# ===== Часовые и полчасовые сообщения =====
async def hourly_message(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(timezone(timedelta(hours=3)))  # Москва +3
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"🕒 Сейчас {now.strftime('%d.%m.%Y %H:%M:%S')}"
    )

async def half_hour_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text="🤫 В чате тишина? Давно не было смешного контента!"
    )

async def meme_or_joke(context: ContextTypes.DEFAULT_TYPE):
    action = random.choice(["meme", "joke"])
    if action == "meme":
        meme_link = get_rss_meme()
        if meme_link:
            await context.bot.send_message(chat_id=CHAT_ID, text=f"🎬 Мем для вас: {meme_link}")
    else:
        joke = random.choice(JOKES_LIST)
        await context.bot.send_message(chat_id=CHAT_ID, text=joke)

# ===== Основная функция =====
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчики
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.VIDEO, on_video))

    # Планировщик
    scheduler = AsyncIOScheduler()
    scheduler.add_job(hourly_message, 'interval', hours=1, args=[app.bot])
    scheduler.add_job(half_hour_message, 'interval', minutes=30, args=[app.bot])
    scheduler.add_job(meme_or_joke, 'interval', hours=1, args=[app.bot])
    scheduler.start()

    await app.run_polling()

# ===== Запуск =====
if __name__ == "__main__":
    asyncio.run(main())
import random
import time
import feedparser
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"
CHAT_ID = -5084894998

# ===== ЮМОР =====
PHOTO_REPLIES = [
    "🖼 Так… это искусство или мем?",
    "📸 Скриншот судьбы принят 😄",
    "😂 Картинка сказала больше, чем слова",
    "🫠 Чат официально стал красивее",
]

VIDEO_REPLIES = [
    "🎬 Попкорн где?",
    "📹 Ну всё, залипли",
    "😂 Видео — лучший аргумент",
    "🫣 Это точно можно смотреть?",
]

JOKES_LIST = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 = DEC 25 😄",
    "Баг — это фича, о которой ты ещё не знаешь 😉",
    "Сначала был кофе, потом код ☕💻",
]

SUBREDDITS_RSS = [
    "https://www.reddit.com/r/memes/.rss",
    "https://www.reddit.com/r/dankmemes/.rss",
    "https://www.reddit.com/r/ProgrammerHumor/.rss",
]

LAST_REPLY_TIME = 0
COOLDOWN = 120


def get_rss_meme():
    feed = feedparser.parse(random.choice(SUBREDDITS_RSS))
    if feed.entries:
        return random.choice(feed.entries).link
    return None


async def can_reply():
    global LAST_REPLY_TIME
    now = time.time()
    if now - LAST_REPLY_TIME > COOLDOWN:
        LAST_REPLY_TIME = now
        return True
    return False


async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and await can_reply():
        await update.message.reply_text(random.choice(PHOTO_REPLIES))


async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and await can_reply():
        await update.message.reply_text(random.choice(VIDEO_REPLIES))


async def hourly_job(context: ContextTypes.DEFAULT_TYPE):
    if random.choice([True, False]):
        meme = get_rss_meme()
        if meme:
            await context.bot.send_message(CHAT_ID, f"😂 Мем часа:\n{meme}")
    else:
        await context.bot.send_message(CHAT_ID, random.choice(JOKES_LIST))


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.VIDEO, on_video))

    app.job_queue.run_repeating(hourly_job, interval=3600, first=10)

    print("🤖 Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()

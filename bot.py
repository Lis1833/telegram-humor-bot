import random
import time
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# ===== Настройки =====
BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"  # токен бота
CHAT_ID = -5084894998                                           # ID группы

# ===== Юморные фразы =====
PHOTO_REPLIES = [
    "🖼 Так… это искусство или мем?",
    "📸 Скриншот судьбы принят 😄",
    "🖌 Вот это поворот!",
    "👀 А вот с этого места поподробнее",
    "😂 Картинка сказала больше, чем слова",
    "🫠 Чат официально стал красивее",
]

VIDEO_REPLIES = [
    "🎬 Попкорн где?",
    "📹 Ну всё, залипли",
    "👀 Сейчас будет что-то интересное",
    "😂 Видео — лучший аргумент",
    "🎞 Надеюсь, без сюжета как в артхаусе",
    "🫣 Это точно можно смотреть?",
]

JOKES_LIST = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 = DEC 25 😄",
    "Баг — это фича, о которой ты ещё не знаешь 😉",
    "Учёные доказали: кофе — источник счастья ☕",
    "Сначала был кофе, потом код ☕💻",
]

# ===== RSS сабреддитов для мемов =====
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

# ===== Обработчики фото и видео =====
async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and await can_reply():
        await update.message.reply_text(random.choice(PHOTO_REPLIES))

async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.5 and await can_reply():
        await update.message.reply_text(random.choice(VIDEO_REPLIES))

# ===== Часовое сообщение =====
async def hourly_message(context: ContextTypes.DEFAULT_TYPE):
    action = random.choice(["meme", "joke"])

    if action == "meme":
        meme_link = get_rss_meme()
        if meme_link:
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text=f"🎬 Мем для вас: {meme_link}"
            )

    elif action == "joke":
        joke = random.choice(JOKES_LIST)
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=joke
        )

# ===== Основная функция =====
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Хендлеры медиа
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.VIDEO, on_video))

    # Планировщик часовых сообщений
    scheduler = AsyncIOScheduler()
    scheduler.add_job(hourly_message, "interval", hours=1, args=[app.bot])
    scheduler.start()

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

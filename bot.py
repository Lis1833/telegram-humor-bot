import random
import asyncio
from datetime import datetime
import pytz

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"
CHAT_ID = -5084894998

MOSCOW_TZ = pytz.timezone("Europe/Moscow")

# ================== РЕАКЦИИ ==================
PHOTO_REPLIES = [
    "📸 Ого, вот это кадр 😂",
    "🖼 Сохраняю себе в память",
    "😂 Это можно пересматривать",
    "👀 А это точно без фотошопа?",
    "🔥 Фото дня",
    "🤣 Чат официально стал лучше",
    "😎 Стильно, модно, молодёжно",
    "🤔 Тут есть над чем подумать",
    "🫠 Я не был готов к этому",
    "😂 Классика",
]

VIDEO_REPLIES = [
    "🎬 Ну всё, залипли",
    "🍿 Где попкорн?",
    "😂 Это видео сделало мой день",
    "👀 С первого раза не понял",
    "🔥 Контент подъехал",
    "🤣 Вот за это я люблю интернет",
    "😳 Неожиданно",
    "🫠 Я пересмотрю ещё раз",
    "😎 Хорош",
    "😂 Сильный ход",
]

SILENCE_MESSAGES = [
    "🤫 В группе тишина… подозрительно",
    "😴 Что-то давно не было смешного",
    "👀 Народ, вы где?",
    "😂 Алё, мемы закончились?",
    "🫠 Чат уснул?",
    "📢 Время для контента!",
]

# ================== ОБРАБОТЧИКИ ==================
async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == CHAT_ID:
        await update.message.reply_text(random.choice(PHOTO_REPLIES))


async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == CHAT_ID:
        await update.message.reply_text(random.choice(VIDEO_REPLIES))


# ================== ЗАДАЧИ ПО РАСПИСАНИЮ ==================
async def silence_job(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=random.choice(SILENCE_MESSAGES),
    )


async def time_job(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(MOSCOW_TZ)
    text = f"🕒 Сейчас в Москве: {now.strftime('%d.%m.%Y %H:%M')}"
    await context.bot.send_message(chat_id=CHAT_ID, text=text)


# ================== MAIN ==================
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.VIDEO, on_video))

    scheduler = AsyncIOScheduler(timezone=MOSCOW_TZ)
    scheduler.add_job(silence_job, "interval", minutes=30, args=[app.bot])
    scheduler.add_job(time_job, "interval", hours=1, args=[app.bot])
    scheduler.start()

    print("✅ Бот запущен")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import WebAppInfo
import os

# Логирование — НАЧАЛО
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# Логирование — КОНЕЦ

# Загрузка переменных из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Команда /start
WEBAPP_URL = os.getenv("WEBAPP_URL")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Готов играть?",
        reply_markup=reply_markup
    )


# Обработка нажатий кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "button_clicked":
        await query.edit_message_text("Ты нажал на кнопку! 😸")
        logger.info(f"Пользователь {query.from_user.username} нажал кнопку.")

# Основная функция запуска
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

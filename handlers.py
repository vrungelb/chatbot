import logging
from telegram import Update
from telegram.ext import ContextTypes

from gigachat_client import get_gigachat_response
from status import build_server_status_text

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Бот запущен.\n"
        "Можешь написать любой текст — я отправлю его в GigaChat.\n\n"
        "Чтобы проверить статус сервера, напиши /status."
    )


async def server_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Собираю статус сервера...")
        status_text = build_server_status_text()
        await update.message.reply_text(status_text)
    except Exception as e:
        logger.exception("Ошибка при получении статуса сервера")
        await update.message.reply_text(f"Не удалось получить статус: {e}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        answer = get_gigachat_response(user_text)
        await update.message.reply_text(answer)
    except Exception as e:
        logger.exception("Ошибка при запросе к GigaChat")
        await update.message.reply_text(f"Ошибка при обращении к GigaChat: {e}")

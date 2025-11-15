import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from gigachat_client import get_gigachat_response
from status import build_server_status_text

logger = logging.getLogger(__name__)


# показываем приветствие и кнопку для проверки сервера
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Статус сервера", callback_data="server_status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Бот запущен.\n"
        "Можешь написать любой текст — я отправлю его в GigaChat.\n\n"
        "Для проверки сервера нажми кнопку ниже:",
        reply_markup=reply_markup,
    )


# обработка любых кнопок, которые приходят как callback_query
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # отвечаем Telegram, что кнопка обработана

    # проверка статуса сервера
    if query.data == "server_status":
        # показываем текст, чтобы пользователь видел, что что-то происходит
        await query.edit_message_text("Собираю статус сервера...")

        try:
            status_text = build_server_status_text()
            await query.message.reply_text(status_text)
        except Exception as e:
            logger.exception("Ошибка при получении статуса сервера")
            await query.message.reply_text(f"Не удалось получить статус: {e}")


# всё, что не команда — отправляем в GigaChat
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        answer = get_gigachat_response(user_text)
        await update.message.reply_text(answer)
    except Exception as e:
        logger.exception("Ошибка при запросе к GigaChat")
        await update.message.reply_text(f"Ошибка при обращении к GigaChat: {e}")

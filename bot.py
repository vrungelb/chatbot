import logging
import os
import subprocess

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from gigachat_client import get_gigachat_response


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ВСТАВЬ_ТУТ_ТВОЙ_ТГ_ТОКЕН")


def build_server_status_text() -> str:
    # Uptime
    try:
        uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()
    except Exception as e:
        uptime = f"не удалось получить (ошибка: {e})"

    # CPU load (одна строка из top)
    try:
        cpu_line = subprocess.check_output(
            "LANG=C top -bn1 | grep Cpu", shell=True
        ).decode().strip()
    except Exception as e:
        cpu_line = f"не удалось получить (ошибка: {e})"

    # RAM usage
    try:
        mem = subprocess.check_output("free -h | grep Mem", shell=True).decode().split()
        total_ram = mem[1] if len(mem) > 1 else "?"
        used_ram = mem[2] if len(mem) > 2 else "?"
        ram_info = f"{used_ram} / {total_ram}"
    except Exception as e:
        ram_info = f"не удалось получить (ошибка: {e})"

    # Интернет
    try:
        requests.get("https://www.google.com", timeout=3)
        internet = "OK"
    except Exception:
        internet = "нет соединения"

    # GigaChat
    try:
        _ = get_gigachat_response("Ответь словом OK.")
        gigachat_status = "OK"
    except Exception as e:
        gigachat_status = f"ошибка: {e}"

    # Telegram API: раз бот выполняет этот код, значит соединение есть
    telegram_status = "OK"

    text = (
        "📊 Статус сервера и бота\n"
        "-------------------------\n"
        f"Telegram API: {telegram_status}\n"
        f"GigaChat: {gigachat_status}\n"
        f"Интернет: {internet}\n"
        "\n"
        "Система:\n"
        f"• Uptime: {uptime}\n"
        f"• CPU: {cpu_line}\n"
        f"• RAM: {ram_info}\n"
        "-------------------------\n"
        "Бот запущен и отвечает на сообщения."
    )

    return text


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Статус сервера", callback_data="server_status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Бот запущен.\n"
        "Можешь написать любой текст — я спрошу GigaChat.\n\n"
        "Для быстрой проверки нажми кнопку ниже:",
        reply_markup=reply_markup,
    )


# обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "server_status":
        await query.edit_message_text("Проверяю статус сервера и GigaChat...")
        try:
            status_text = build_server_status_text()
            await query.message.reply_text(status_text)
        except Exception as e:
            logger.exception("Ошибка при получении статуса сервера")
            await query.message.reply_text(f"Ошибка при получении статуса: {e}")


# любой текст → в GigaChat
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        answer = get_gigachat_response(user_text)
        await update.message.reply_text(answer)
    except Exception as e:
        logger.exception("Ошибка при запросе к GigaChat")
        await update.message.reply_text(f"Ошибка при обращении к GigaChat: {e}")


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logging.info("Бот запущен (polling).")
    app.run_polling()


if __name__ == "__main__":
    main()

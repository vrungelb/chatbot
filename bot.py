import logging
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from handlers import start, button_handler, handle_text


logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def main():
    # инициализация приложения бота
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # регистрируем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # регистрируем обработчик нажатий на inline-кнопки
    app.add_handler(CallbackQueryHandler(button_handler))

    # регистрируем обработчик обычного текста
    # сюда попадает всё, что не команда
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # запускаем бота в режиме long polling
    logger.info("бот запущен и ждёт обновления")
    app.run_polling()


if __name__ == "__main__":
    main()

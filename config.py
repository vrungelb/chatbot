import os
from pathlib import Path
from dotenv import load_dotenv

# загружаем .env рядом с проектом
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)


def require_env(name: str) -> str:
    """возвращает переменную окружения или кидает понятную ошибку"""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"env var {name} is not set")
    return value


# обязательные переменные
TELEGRAM_BOT_TOKEN = require_env("TELEGRAM_BOT_TOKEN")

# gigachat
GIGACHAT_CREDENTIALS = require_env("GIGACHAT_CREDENTIALS")
GIGACHAT_SCOPE = require_env("GIGACHAT_SCOPE")

# yandex cloud
YC_FOLDER_ID = require_env("YC_FOLDER_ID")
YC_API_KEY = require_env("YC_API_KEY")

# выбор моделей
AI_PRIMARY = os.getenv("AI_PRIMARY", "giga").lower()
AI_SECONDARY = os.getenv("AI_SECONDARY", "yandex").lower()

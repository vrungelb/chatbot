#!/usr/bin/env bash

# 1. Загружаем переменные окружения из .env
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# 2. Активируем виртуальное окружение
source venv/bin/activate

# 3. Запускаем бота
python bot.py

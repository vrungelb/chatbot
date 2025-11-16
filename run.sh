#!/usr/bin/env bash

set -e  # если чето падает, сразу выходим

# переходим в каталог проекта
cd /root/telegram_gigachat_bot

# загружаем переменные окружения из .env
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# активируем виртуальное окружение
source venv/bin/activate

PIDFILE="bot.pid"

# проверяем, не запущен ли бот уже
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")

    if kill -0 "$PID" 2>/dev/null; then
        # доп.проверка, что это именно наш бот
        CMD=$(ps -p "$PID" -o cmd= 2>/dev/null || echo "")

        if echo "$CMD" | grep -q "python bot.py"; then
            echo "Bot is already running with PID $PID"
            exit 1
        else
            echo "PID file exists, but process is not bot. Removing stale PID."
            rm "$PIDFILE"
        fi
    else
        echo "PID file exists, but no running process. Removing stale PID."
        rm "$PIDFILE"
    fi
fi

# запускаем бота в фоне через nohup
nohup python bot.py >> bot.log 2>&1 &
PID=$!

# сохраняем PID
echo "$PID" > "$PIDFILE"

echo "Bot started with PID $PID"

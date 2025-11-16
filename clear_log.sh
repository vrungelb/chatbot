#!/bin/bash

LOG_FILE="/root/telegram_gigachat_bot/bot.log"

if [ -f "$LOG_FILE" ]; then
    # очистить файл, но не удалять его
    > "$LOG_FILE"
fi

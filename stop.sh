#!/usr/bin/env bash

cd /root/telegram_gigachat_bot

PIDFILE="bot.pid"

if [ ! -f "$PIDFILE" ]; then
    echo "No PID file found"
    exit 1
fi

PID=$(cat "$PIDFILE")

if kill -0 "$PID" 2>/dev/null; then
    echo "Stopping bot PID $PID"
    kill "$PID"
else
    echo "Process already dead"
fi

rm "$PIDFILE"

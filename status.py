import subprocess
import requests
from gigachat_client import get_gigachat_response


# возврат статусных точек
def _status_icon(ok: bool) -> str:
    return "🟢" if ok else "🔴"


def build_server_status_text() -> str:
    # uptime сколько сервер живёт после последней перезагрузки
    try:
        uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()
        uptime_ok = True
    except:
        uptime = "ошибка"
        uptime_ok = False

    # берём первую строку с данными о загрузке CPU
    try:
        cpu_line = subprocess.check_output(
            "LANG=C top -bn1 | grep Cpu", shell=True
        ).decode().strip()
        cpu_ok = True
    except:
        cpu_line = "ошибка"
        cpu_ok = False

    # объём RAM: занято / всего
    try:
        mem = subprocess.check_output("free -h | grep Mem", shell=True).decode().split()
        ram = f"{mem[2]} / {mem[1]}"
        ram_ok = True
    except:
        ram = "ошибка"
        ram_ok = False

    # есть ли вообще интернет
    try:
        requests.get("https://www.google.com", timeout=3)
        internet_ok = True
    except:
        internet_ok = False

    # отвечает ли GigaChat, т.е. делаем короткий запрос
    try:
        get_gigachat_response("OK?")
        giga_ok = True
    except:
        giga_ok = False

    # Если бот работает — Telegram доступен, отдельно проверять смысла нет
    telegram_ok = True

    # Собираем единый текст для отправки
    text = (
        "📊 **Статус сервера**\n"
        "-------------------------\n"
        f"{_status_icon(telegram_ok)} Telegram API\n"
        f"{_status_icon(giga_ok)} GigaChat API\n"
        f"{_status_icon(internet_ok)} Интернет\n"
        "\n"
        "🖥 **Система**\n"
        f"{_status_icon(uptime_ok)} Uptime: {uptime}\n"
        f"{_status_icon(cpu_ok)} CPU: {cpu_line}\n"
        f"{_status_icon(ram_ok)} RAM: {ram}\n"
        "-------------------------\n"
        "Готов к работе."
    )

    return text

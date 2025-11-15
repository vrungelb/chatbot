# gigachat_client.py

import os
from gigachat import GigaChat


# Читаем Authorization Key и scope из переменных окружения
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")


def get_gigachat_response(prompt: str) -> str:
    """
    Отправляет строку в GigaChat и возвращает текст ответа.
    Работает только через переменные окружения — ни один токен в коде не хранится.
    """

    if not GIGACHAT_CREDENTIALS:
        raise RuntimeError(
            "GIGACHAT_CREDENTIALS не задан. Установи Authorization Key GigaChat:\n"
            "export GIGACHAT_CREDENTIALS=\"...\""
        )

    with GigaChat(
        credentials=GIGACHAT_CREDENTIALS,
        scope=GIGACHAT_SCOPE,
        verify_ssl_certs=False,  # для тестов; позже можно включить True
    ) as giga:
        response = giga.chat(prompt)

    if not response.choices:
        return "GigaChat не вернул ответа."

    return response.choices[0].message.content

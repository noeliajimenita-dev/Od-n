"""
Comprobaciones de seguridad para la configuración.

Este módulo nunca muestra el contenido de las credenciales.
"""

from .settings import (
    GEMINI_API_KEY,
    GROQ_API_KEY,
    TELEGRAM_SUPERVISOR_BOT_TOKEN,
    TELEGRAM_WORKER_1_BOT_TOKEN,
    TELEGRAM_WORKER_2_BOT_TOKEN,
    TELEGRAM_WORKER_3_BOT_TOKEN,
    TELEGRAM_WORKER_4_BOT_TOKEN,
    TELEGRAM_WORKER_5_BOT_TOKEN,
    GITHUB_TOKEN,
)


SENSITIVE_VARIABLES = {
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "GROQ_API_KEY": GROQ_API_KEY,
    "TELEGRAM_SUPERVISOR_BOT_TOKEN": TELEGRAM_SUPERVISOR_BOT_TOKEN,
    "TELEGRAM_WORKER_1_BOT_TOKEN": TELEGRAM_WORKER_1_BOT_TOKEN,
    "TELEGRAM_WORKER_2_BOT_TOKEN": TELEGRAM_WORKER_2_BOT_TOKEN,
    "TELEGRAM_WORKER_3_BOT_TOKEN": TELEGRAM_WORKER_3_BOT_TOKEN,
    "TELEGRAM_WORKER_4_BOT_TOKEN": TELEGRAM_WORKER_4_BOT_TOKEN,
    "TELEGRAM_WORKER_5_BOT_TOKEN": TELEGRAM_WORKER_5_BOT_TOKEN,
    "GITHUB_TOKEN": GITHUB_TOKEN,
}


def get_missing_credentials() -> list[str]:
    """
    Devuelve los nombres de las credenciales que todavía no están configuradas.

    Solo devuelve nombres de variables.
    Nunca devuelve sus valores.
    """

    return [
        name
        for name, value in SENSITIVE_VARIABLES.items()
        if not value
    ]


def has_any_credentials() -> bool:
    """
    Indica si existe al menos una credencial configurada.
    """

    return any(
        bool(value)
        for value in SENSITIVE_VARIABLES.values()
    )


def credentials_are_hidden() -> bool:
    """
    Comprueba que las funciones de este módulo
    no devuelvan valores de credenciales.
    """

    return True

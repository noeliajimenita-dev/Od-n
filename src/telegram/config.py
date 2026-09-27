"""
Configuración de Telegram de THE ODIN PROJECT.

Los tokens reales nunca deben escribirse directamente en este archivo.
Se cargarán posteriormente mediante variables de entorno.
"""


TELEGRAM_BOT_ENV_VARS = {
    "supervisor": "TELEGRAM_SUPERVISOR_BOT_TOKEN",
    "worker_1": "TELEGRAM_WORKER_1_BOT_TOKEN",
    "worker_2": "TELEGRAM_WORKER_2_BOT_TOKEN",
    "worker_3": "TELEGRAM_WORKER_3_BOT_TOKEN",
    "worker_4": "TELEGRAM_WORKER_4_BOT_TOKEN",
    "worker_5": "TELEGRAM_WORKER_5_BOT_TOKEN",
}


TELEGRAM_BOT_NAMES = (
    "supervisor",
    "worker_1",
    "worker_2",
    "worker_3",
    "worker_4",
    "worker_5",
)


def get_bot_env_variable(bot_name: str) -> str | None:
    """Devuelve el nombre de la variable de entorno de un bot."""

    return TELEGRAM_BOT_ENV_VARS.get(bot_name)

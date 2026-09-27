from .bot import TelegramBot
from .config import TELEGRAM_BOT_ENV_VARS, TELEGRAM_BOT_NAMES


def create_bot_registry() -> dict[str, TelegramBot]:
    """Crea el registro de los seis bots del sistema."""

    return {
        bot_name: TelegramBot(
            name=bot_name,
            token_env_variable=TELEGRAM_BOT_ENV_VARS[bot_name],
        )
        for bot_name in TELEGRAM_BOT_NAMES
    }


def get_bot(
    bot_name: str,
    registry: dict[str, TelegramBot],
) -> TelegramBot | None:
    """Obtiene un bot por su nombre."""

    return registry.get(bot_name)


def get_enabled_bots(
    registry: dict[str, TelegramBot],
) -> list[TelegramBot]:
    """Devuelve los bots actualmente habilitados."""

    return [
        bot
        for bot in registry.values()
        if bot.enabled
    ]

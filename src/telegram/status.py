from .bot import TelegramBot
from .registry import create_bot_registry


def get_telegram_status(
    registry: dict[str, TelegramBot] | None = None,
) -> dict:
    """Devuelve un resumen del estado de los bots de Telegram."""

    if registry is None:
        registry = create_bot_registry()

    bots = list(registry.values())

    enabled = [
        bot for bot in bots
        if bot.enabled
    ]

    configured = [
        bot for bot in bots
        if bot.is_configured()
    ]

    return {
        "total_bots": len(bots),
        "enabled_bots": len(enabled),
        "configured_bots": len(configured),
        "bots": [bot.name for bot in bots],
    }

from .bot_status import TelegramBotStatus
from .registry import create_bot_registry
from .token_loader import load_bot_token


def get_bot_registry_status() -> list[TelegramBotStatus]:
    registry = create_bot_registry()
    statuses = []

    for bot_name, bot in registry.items():
        token_configured = False

        try:
            load_bot_token(bot.token_env_variable)
            token_configured = True
        except ValueError:
            token_configured = False

        statuses.append(
            TelegramBotStatus(
                bot_name=bot_name,
                enabled=bot.enabled,
                token_configured=token_configured,
            )
        )

    return statuses

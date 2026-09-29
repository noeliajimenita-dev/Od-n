from dataclasses import dataclass

from .connection_session import TelegramConnectionSession


@dataclass(frozen=True)
class TelegramConnectionHealth:
    bot_name: str
    healthy: bool
    connected: bool
    reason: str


def check_connection_health(
    session: TelegramConnectionSession,
) -> TelegramConnectionHealth:
    if session.is_connected():
        return TelegramConnectionHealth(
            bot_name=session.bot_name,
            healthy=True,
            connected=True,
            reason="Conexión activa.",
        )

    return TelegramConnectionHealth(
        bot_name=session.bot_name,
        healthy=False,
        connected=False,
        reason="El bot no está conectado.",
    )

from .connection_registry import TelegramConnectionRegistry


def get_connection_registry_status(
    registry: TelegramConnectionRegistry,
) -> dict:
    sessions = registry.get_all()

    connected_bots = [
        bot_name
        for bot_name, session in sessions.items()
        if session.is_connected()
    ]

    return {
        "total_sessions": len(sessions),
        "connected_sessions": len(connected_bots),
        "disconnected_sessions": len(sessions) - len(connected_bots),
        "connected_bots": connected_bots,
    }

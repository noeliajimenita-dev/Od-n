from .connection_registry import TelegramConnectionRegistry
from .connection_health import check_connection_health


def get_connection_recovery_status(
    registry: TelegramConnectionRegistry,
) -> dict:
    sessions = registry.get_all()

    needs_recovery = []
    recovered = []

    for bot_name, session in sessions.items():
        health = check_connection_health(session)

        if health.healthy:
            recovered.append(bot_name)
        else:
            needs_recovery.append(bot_name)

    return {
        "total_bots": len(sessions),
        "recovered_bots": len(recovered),
        "bots_needing_recovery": len(needs_recovery),
        "recovered_bot_names": recovered,
        "bots_needing_recovery_names": needs_recovery,
    }

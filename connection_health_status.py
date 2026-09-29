from .connection_registry import TelegramConnectionRegistry
from .connection_health import check_connection_health


def get_connection_health_status(
    registry: TelegramConnectionRegistry,
) -> dict:
    sessions = registry.get_all()

    health_results = [
        check_connection_health(session)
        for session in sessions.values()
    ]

    healthy_bots = [
        result.bot_name
        for result in health_results
        if result.healthy
    ]

    unhealthy_bots = [
        result.bot_name
        for result in health_results
        if not result.healthy
    ]

    return {
        "total_bots": len(health_results),
        "healthy_bots": len(healthy_bots),
        "unhealthy_bots": len(unhealthy_bots),
        "healthy_bot_names": healthy_bots,
        "unhealthy_bot_names": unhealthy_bots,
    }

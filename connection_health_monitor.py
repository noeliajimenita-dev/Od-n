from .connection_registry import TelegramConnectionRegistry
from .connection_health import check_connection_health


class TelegramConnectionHealthMonitor:
    def __init__(self, registry: TelegramConnectionRegistry):
        self.registry = registry

    def check_all(self) -> dict:
        sessions = self.registry.get_all()

        results = {}

        for bot_name, session in sessions.items():
            health = check_connection_health(session)

            results[bot_name] = {
                "healthy": health.healthy,
                "connected": health.connected,
                "reason": health.reason,
            }

        return results

    def unhealthy_bots(self) -> list[str]:
        results = self.check_all()

        return [
            bot_name
            for bot_name, health in results.items()
            if not health["healthy"]
        ]

    def all_healthy(self) -> bool:
        return len(self.unhealthy_bots()) == 0

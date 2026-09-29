from .connection_service import TelegramConnectionService
from .connection_service_status import get_connection_service_status


class TelegramConnectionSupervisor:
    def __init__(self, service: TelegramConnectionService):
        self.service = service

    def inspect(self) -> dict:
        return get_connection_service_status(self.service)

    def disconnected_bots(self) -> list[str]:
        status = self.inspect()
        return status["disconnected_bot_names"]

    def connected_bots(self) -> list[str]:
        status = self.inspect()
        return status["connected_bot_names"]

    def all_connected(self) -> bool:
        status = self.inspect()

        return (
            status["total_bots"] > 0
            and status["disconnected_bots"] == 0
        )

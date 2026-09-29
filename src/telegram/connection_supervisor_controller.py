from .connection_supervisor import TelegramConnectionSupervisor


class TelegramConnectionSupervisorController:
    def __init__(self, supervisor: TelegramConnectionSupervisor):
        self.supervisor = supervisor

    def connect_bot(self, bot_name: str) -> None:
        self.supervisor.service.connect(bot_name)

    def disconnect_bot(self, bot_name: str) -> None:
        self.supervisor.service.disconnect(bot_name)

    def recover_bot(self, bot_name: str) -> None:
        self.supervisor.service.recover(bot_name)

    def get_connected_bots(self) -> list[str]:
        return self.supervisor.connected_bots()

    def get_disconnected_bots(self) -> list[str]:
        return self.supervisor.disconnected_bots()

    def all_connected(self) -> bool:
        return self.supervisor.all_connected()

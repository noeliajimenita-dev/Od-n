from .connection_controller import TelegramConnectionController


class TelegramConnectionRecovery:
    def __init__(self, controller: TelegramConnectionController):
        self.controller = controller

    def recover(self, enabled: bool = True) -> bool:
        if self.controller.is_connected():
            return True

        self.controller.connect(enabled=enabled)

        return self.controller.is_connected()

    def is_recovered(self) -> bool:
        return self.controller.is_connected()

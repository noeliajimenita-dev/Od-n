from .connection_controller import TelegramConnectionController
from .connection_registry import TelegramConnectionRegistry


class TelegramConnectionService:
    def __init__(
        self,
        registry: TelegramConnectionRegistry,
        controllers: dict[str, TelegramConnectionController],
    ):
        self.registry = registry
        self.controllers = controllers

    def connect_bot(self, bot_name: str, enabled: bool = True) -> None:
        controller = self._get_controller(bot_name)
        controller.connect(enabled=enabled)

    def disconnect_bot(self, bot_name: str) -> None:
        controller = self._get_controller(bot_name)
        controller.disconnect()

    def is_connected(self, bot_name: str) -> bool:
        controller = self._get_controller(bot_name)
        return controller.is_connected()

    def get_status(self, bot_name: str) -> dict:
        controller = self._get_controller(bot_name)
        return controller.status()

    def get_all_status(self) -> dict[str, dict]:
        return {
            bot_name: controller.status()
            for bot_name, controller in self.controllers.items()
        }

    def _get_controller(
        self,
        bot_name: str,
    ) -> TelegramConnectionController:
        if bot_name not in self.controllers:
            raise KeyError(f"Controlador no encontrado: {bot_name}")

        return self.controllers[bot_name]

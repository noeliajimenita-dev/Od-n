from .client import TelegramClient


class TelegramConnectionGuard:
    def __init__(self, client: TelegramClient):
        self.client = client

    def can_connect(self) -> bool:
        return self.client.is_ready()

    def require_connection(self) -> None:
        if not self.can_connect():
            raise RuntimeError(
                f"El bot '{self.client.bot_name}' no está configurado "
                "o no tiene un token disponible."
            )

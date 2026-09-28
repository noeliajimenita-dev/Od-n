from .client import TelegramClient
from .registry import create_bot_registry


class TelegramManager:
    def __init__(self):
        self.registry = create_bot_registry()
        self.clients = {
            bot_name: TelegramClient(
                bot_name=bot.name,
                token_env_variable=bot.token_env_variable,
            )
            for bot_name, bot in self.registry.items()
        }

    def get_client(self, bot_name: str) -> TelegramClient:
        if bot_name not in self.clients:
            raise KeyError(f"Bot no encontrado: {bot_name}")

        return self.clients[bot_name]

    def get_all_clients(self) -> dict[str, TelegramClient]:
        return dict(self.clients)

    def get_ready_bots(self) -> list[str]:
        return [
            name
            for name, client in self.clients.items()
            if client.is_ready()
        ]

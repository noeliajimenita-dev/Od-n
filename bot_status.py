from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramBotStatus:
    bot_name: str
    enabled: bool
    token_configured: bool
    connected: bool = False

    def is_ready(self) -> bool:
        return self.enabled and self.token_configured

    def is_connected(self) -> bool:
        return self.connected

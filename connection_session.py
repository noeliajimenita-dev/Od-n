from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class TelegramConnectionSession:
    bot_name: str
    connected: bool = False
    connected_at: datetime | None = None

    def connect(self) -> None:
        if self.connected:
            return

        self.connected = True
        self.connected_at = datetime.now(timezone.utc)

    def disconnect(self) -> None:
        self.connected = False
        self.connected_at = None

    def is_connected(self) -> bool:
        return self.connected

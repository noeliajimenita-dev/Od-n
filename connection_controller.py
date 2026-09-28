from .connection_guard import TelegramConnectionGuard
from .connection_policy import TelegramConnectionPolicy
from .connection_session import TelegramConnectionSession


class TelegramConnectionController:
    def __init__(
        self,
        guard: TelegramConnectionGuard,
        policy: TelegramConnectionPolicy,
        session: TelegramConnectionSession,
    ):
        self.guard = guard
        self.policy = policy
        self.session = session

    def connect(self, enabled: bool = True) -> None:
        self.policy.validate(self.guard, enabled=enabled)
        self.session.connect()

    def disconnect(self) -> None:
        self.session.disconnect()

    def is_connected(self) -> bool:
        return self.session.is_connected()

    def status(self) -> dict:
        return {
            "bot_name": self.session.bot_name,
            "connected": self.session.is_connected(),
            "connected_at": self.session.connected_at,
        }

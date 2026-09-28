from dataclasses import dataclass

from .connection_guard import TelegramConnectionGuard


@dataclass(frozen=True)
class TelegramConnectionPolicy:
    require_token: bool = True
    require_enabled: bool = True

    def can_connect(self, guard: TelegramConnectionGuard, enabled: bool = True) -> bool:
        if self.require_enabled and not enabled:
            return False

        if self.require_token and not guard.can_connect():
            return False

        return True

    def validate(
        self,
        guard: TelegramConnectionGuard,
        enabled: bool = True,
    ) -> None:
        if not self.can_connect(guard, enabled):
            raise RuntimeError(
                "La política de conexión de Telegram no permite "
                "establecer la conexión."
            )

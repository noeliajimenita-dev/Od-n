from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramBot:
    """Representa un bot de Telegram del sistema."""

    name: str
    token_env_variable: str
    enabled: bool = True

    def is_configured(self) -> bool:
        """Indica si el bot tiene definida una variable de entorno."""

        return bool(self.token_env_variable)

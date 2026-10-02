from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramBotConfig:
    """
    Configuración de un bot de Telegram.

    El token nunca debe escribirse directamente en este archivo.
    Debe llegar desde variables de entorno o desde un gestor seguro
    de credenciales.
    """

    bot_name: str
    token: str
    chat_id: str | None = None
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.bot_name or not self.bot_name.strip():
            raise ValueError("bot_name cannot be empty")

        if not self.token or not self.token.strip():
            raise ValueError("token cannot be empty")

        if self.chat_id is not None and not str(self.chat_id).strip():
            raise ValueError("chat_id cannot be empty")

    def masked_token(self) -> str:
        """
        Devuelve una representación segura del token.

        Nunca devuelve el token completo.
        """
        token = self.token

        if len(token) <= 8:
            return "*" * len(token)

        return f"{token[:4]}...{token[-4:]}"

    def to_dict(self) -> dict[str, object]:
        """
        Serialización segura para logs y estados.

        El token real nunca aparece.
        """
        return {
            "bot_name": self.bot_name,
            "token": self.masked_token(),
            "chat_id": self.chat_id,
            "enabled": self.enabled,
        }


class TelegramConfig:
    """
    Registro central de configuraciones Telegram.

    Permite administrar Supervisor + Workers sin guardar tokens
    dentro del código fuente.
    """

    ENV_PREFIX = "ODIN_TELEGRAM_"

    def __init__(self) -> None:
        self._bots: dict[str, TelegramBotConfig] = {}

    def register(
        self,
        bot_name: str,
        token: str,
        chat_id: str | None = None,
        enabled: bool = True,
    ) -> TelegramBotConfig:
        """Registra o reemplaza la configuración de un bot."""
        config = TelegramBotConfig(
            bot_name=bot_name,
            token=token,
            chat_id=chat_id,
            enabled=enabled,
        )

        self._bots[bot_name] = config
        return config

    def register_from_environment(
        self,
        bot_name: str,
        token_variable: str,
        chat_variable: str | None = None,
        enabled: bool = True,
    ) -> TelegramBotConfig:
        """
        Carga un bot desde variables de entorno.

        Ejemplo:

        ODIN_TELEGRAM_SUPERVISOR_TOKEN
        ODIN_TELEGRAM_SUPERVISOR_CHAT_ID
        """
        token = os.getenv(token_variable)

        if not token:
            raise ValueError(
                f"Telegram token environment variable not found: "
                f"{token_variable}"
            )

        chat_id = None

        if chat_variable:
            chat_id = os.getenv(chat_variable)

        return self.register(
            bot_name=bot_name,
            token=token,
            chat_id=chat_id,
            enabled=enabled,
        )

    def get(self, bot_name: str) -> TelegramBotConfig | None:
        """Obtiene la configuración de un bot."""
        return self._bots.get(bot_name)

    def exists(self, bot_name: str) -> bool:
        """Comprueba si un bot está registrado."""
        return bot_name in self._bots

    def remove(self, bot_name: str) -> bool:
        """Elimina una configuración."""
        if bot_name not in self._bots:
            return False

        del self._bots[bot_name]
        return True

    def list_bots(self) -> list[str]:
        """Lista los nombres de bots registrados."""
        return list(self._bots.keys())

    def list_enabled(self) -> list[str]:
        """Lista únicamente los bots habilitados."""
        return [
            name
            for name, config in self._bots.items()
            if config.enabled
        ]

    def count(self) -> int:
        """Cantidad total de bots configurados."""
        return len(self._bots)

    def count_enabled(self) -> int:
        """Cantidad de bots habilitados."""
        return len(self.list_enabled())

    def status(self) -> dict[str, object]:
        """
        Estado seguro de toda la configuración Telegram.

        Los tokens son enmascarados.
        """
        return {
            "total_bots": self.count(),
            "enabled_bots": self.count_enabled(),
            "bots": {
                name: config.to_dict()
                for name, config in self._bots.items()
            },
        }

    def clear(self) -> None:
        """Limpia las configuraciones cargadas en memoria."""
        self._bots.clear()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(bots={self.count()}, enabled={self.count_enabled()})"
  )

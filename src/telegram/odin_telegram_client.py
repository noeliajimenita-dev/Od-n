from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .odin_telegram_config import TelegramBotConfig


class TelegramTransport(Protocol):
    """Contrato para el transporte real de Telegram."""

    def send_message(
        self,
        token: str,
        chat_id: str,
        text: str,
    ) -> Any:
        ...

    def get_updates(
        self,
        token: str,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        ...


@dataclass(frozen=True)
class TelegramMessage:
    """Mensaje normalizado recibido desde Telegram."""

    update_id: int
    chat_id: str
    text: str
    username: str | None = None
    bot_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "update_id": self.update_id,
            "chat_id": self.chat_id,
            "text": self.text,
            "username": self.username,
            "bot_name": self.bot_name,
        }


class TelegramClient:
    """
    Cliente central de comunicación de ODIN.

    No contiene tokens ni credenciales propias.
    Recibe TelegramBotConfig y un transporte externo.
    """

    def __init__(
        self,
        config: TelegramBotConfig,
        transport: TelegramTransport,
    ) -> None:
        if config is None:
            raise ValueError("config cannot be None")

        if transport is None:
            raise ValueError("transport cannot be None")

        self.config = config
        self.transport = transport
        self._last_update_id: int | None = None

    @property
    def bot_name(self) -> str:
        return self.config.bot_name

    @property
    def enabled(self) -> bool:
        return self.config.enabled

    @property
    def last_update_id(self) -> int | None:
        return self._last_update_id

    def send(
        self,
        text: str,
        chat_id: str | None = None,
    ) -> Any:
        """
        Envía un mensaje a Telegram.

        Si no se proporciona chat_id utiliza el configurado
        para el bot.
        """
        if not self.enabled:
            raise RuntimeError(
                f"Telegram bot is disabled: {self.bot_name}"
            )

        if not text or not text.strip():
            raise ValueError("text cannot be empty")

        destination = chat_id or self.config.chat_id

        if not destination:
            raise ValueError(
                "chat_id is required to send a Telegram message"
            )

        return self.transport.send_message(
            token=self.config.token,
            chat_id=str(destination),
            text=text,
        )

    def receive(
        self,
        offset: int | None = None,
    ) -> list[TelegramMessage]:
        """
        Obtiene actualizaciones y las convierte a mensajes ODIN.
        """
        if not self.enabled:
            return []

        selected_offset = (
            offset
            if offset is not None
            else self._next_offset()
        )

        updates = self.transport.get_updates(
            token=self.config.token,
            offset=selected_offset,
        )

        messages: list[TelegramMessage] = []

        for update in updates:
            message = self._parse_update(update)

            if message is None:
                continue

            messages.append(message)

            self._last_update_id = max(
                self._last_update_id or message.update_id,
                message.update_id,
            )

        return messages

    def send_status(
        self,
        status: str,
        chat_id: str | None = None,
    ) -> Any:
        """Envía un estado operativo simple."""
        if not status or not status.strip():
            raise ValueError("status cannot be empty")

        return self.send(
            text=status.strip(),
            chat_id=chat_id,
        )

    def _next_offset(self) -> int | None:
        if self._last_update_id is None:
            return None

        return self._last_update_id + 1

    def _parse_update(
        self,
        update: dict[str, Any],
    ) -> TelegramMessage | None:
        """
        Convierte una actualización de Telegram en un mensaje.

        Las actualizaciones que no contienen texto se ignoran aquí;
        posteriormente M28 podrá incorporar imágenes y archivos
        mediante handlers especializados.
        """
        if not isinstance(update, dict):
            return None

        update_id = update.get("update_id")

        if update_id is None:
            return None

        message_data = update.get("message")

        if not isinstance(message_data, dict):
            return None

        text = message_data.get("text")

        if text is None:
            return None

        chat = message_data.get("chat") or {}
        user = message_data.get("from") or {}

        chat_id = chat.get("id")

        if chat_id is None:
            return None

        username = user.get("username")

        return TelegramMessage(
            update_id=int(update_id),
            chat_id=str(chat_id),
            text=str(text),
            username=str(username) if username else None,
            bot_name=self.bot_name,
        )

    def reset_offset(self) -> None:
        """Reinicia el cursor local de actualizaciones."""
        self._last_update_id = None

    def safe_status(self) -> dict[str, Any]:
        """
        Estado seguro del cliente.

        Nunca expone el token real.
        """
        return {
            "bot_name": self.bot_name,
            "enabled": self.enabled,
            "chat_id": self.config.chat_id,
            "last_update_id": self._last_update_id,
            "token": self.config.masked_token(),
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(bot_name={self.bot_name!r}, "
            f"enabled={self.enabled})"
  )

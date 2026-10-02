from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class TelegramMessageType(str, Enum):
    COMMAND = "command"
    TEXT = "text"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TelegramRoute:
    """Resultado de clasificación de un mensaje."""

    message_type: TelegramMessageType
    target: str
    text: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_type": self.message_type.value,
            "target": self.target,
            "text": self.text,
            "metadata": dict(self.metadata),
        }


class TelegramMessageRouter:
    """
    Router central de mensajes de ODIN.

    Este componente clasifica y enruta mensajes, pero no ejecuta
    directamente acciones sensibles.
    """

    DEFAULT_COMMANDS = {
        "approved",
        "genehmigt",
        "aprobado",
        "rejected",
        "declined",
        "abgelehnt",
        "abgewiesen",
        "redo",
        "rework",
        "überarbeiten",
        "neu machen",
        "pause",
        "hold",
        "stopp",
        "pausar",
        "resume",
        "back to normal",
        "weitermachen",
        "reanudar",
    }

    def __init__(
        self,
        command_handler: Callable[[str, str], Any] | None = None,
        message_handler: Callable[[str, str], Any] | None = None,
    ) -> None:
        self.command_handler = command_handler
        self.message_handler = message_handler

        self._routes: list[TelegramRoute] = []

    def classify(
        self,
        text: str,
    ) -> TelegramMessageType:
        """Clasifica un texto sin ejecutar ninguna acción."""
        normalized = self._normalize(text)

        if not normalized:
            return TelegramMessageType.UNKNOWN

        if normalized in self.DEFAULT_COMMANDS:
            return TelegramMessageType.COMMAND

        if normalized.startswith("/"):
            return TelegramMessageType.COMMAND

        return TelegramMessageType.TEXT

    def route(
        self,
        chat_id: str,
        text: str,
    ) -> TelegramRoute:
        """
        Clasifica y registra una ruta.

        No ejecuta automáticamente acciones sensibles.
        """
        if not chat_id or not str(chat_id).strip():
            raise ValueError("chat_id cannot be empty")

        if not text or not text.strip():
            raise ValueError("text cannot be empty")

        message_type = self.classify(text)

        target = self._resolve_target(
            message_type=message_type,
            text=text,
        )

        route = TelegramRoute(
            message_type=message_type,
            target=target,
            text=text.strip(),
            metadata={
                "chat_id": str(chat_id),
            },
        )

        self._routes.append(route)

        return route

    def dispatch(
        self,
        chat_id: str,
        text: str,
    ) -> Any:
        """
        Clasifica y entrega el mensaje al handler correspondiente.

        Si no existe handler, devuelve la ruta para que otra capa
        pueda procesarla.
        """
        route = self.route(
            chat_id=chat_id,
            text=text,
        )

        if route.message_type == TelegramMessageType.COMMAND:
            if self.command_handler is None:
                return route

            return self.command_handler(
                route.text,
                chat_id,
            )

        if route.message_type == TelegramMessageType.TEXT:
            if self.message_handler is None:
                return route

            return self.message_handler(
                route.text,
                chat_id,
            )

        return route

    def register_command_handler(
        self,
        handler: Callable[[str, str], Any],
    ) -> None:
        """Registra el procesador de comandos."""
        if handler is None:
            raise ValueError("handler cannot be None")

        self.command_handler = handler

    def register_message_handler(
        self,
        handler: Callable[[str, str], Any],
    ) -> None:
        """Registra el procesador de mensajes normales."""
        if handler is None:
            raise ValueError("handler cannot be None")

        self.message_handler = handler

    def add_command(
        self,
        command: str,
    ) -> None:
        """
        Añade un comando reconocido.

        La normalización permite comandos en mayúsculas/minúsculas
        y con espacios redundantes.
        """
        normalized = self._normalize(command)

        if not normalized:
            raise ValueError("command cannot be empty")

        self.DEFAULT_COMMANDS.add(normalized)

    def get_routes(self) -> list[TelegramRoute]:
        """Devuelve una copia del historial de rutas."""
        return list(self._routes)

    def clear_routes(self) -> None:
        """Limpia el historial de rutas en memoria."""
        self._routes.clear()

    def count_routes(self) -> int:
        """Cantidad de mensajes clasificados."""
        return len(self._routes)

    def _resolve_target(
        self,
        message_type: TelegramMessageType,
        text: str,
    ) -> str:
        if message_type == TelegramMessageType.COMMAND:
            return "command_handler"

        if message_type == TelegramMessageType.TEXT:
            return "message_handler"

        return "unknown"

    @staticmethod
    def _normalize(text: str) -> str:
        if text is None:
            return ""

        return " ".join(
            str(text).strip().lower().split()
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(routes={self.count_routes()})"
  )

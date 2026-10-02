from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class OdinCommand(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REDO = "REDO"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class CommandRequest:
    command: OdinCommand
    raw_text: str
    chat_id: str
    argument: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command.value,
            "raw_text": self.raw_text,
            "chat_id": self.chat_id,
            "argument": self.argument,
        }


@dataclass(frozen=True)
class CommandResult:
    command: OdinCommand
    accepted: bool
    message: str
    data: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command.value,
            "accepted": self.accepted,
            "message": self.message,
            "data": self.data,
        }


class TelegramCommandHandler:
    """
    Procesador de comandos de ODIN.

    Su responsabilidad es interpretar y delegar.

    No contiene lógica para gastar dinero, entregar trabajos,
    modificar credenciales ni realizar otras acciones sensibles.
    """

    COMMANDS = {
        "approved": OdinCommand.APPROVE,
        "genehmigt": OdinCommand.APPROVE,
        "aprobado": OdinCommand.APPROVE,

        "rejected": OdinCommand.REJECT,
        "declined": OdinCommand.REJECT,
        "abgelehnt": OdinCommand.REJECT,
        "abgewiesen": OdinCommand.REJECT,

        "redo": OdinCommand.REDO,
        "rework": OdinCommand.REDO,
        "überarbeiten": OdinCommand.REDO,
        "neu machen": OdinCommand.REDO,

        "pause": OdinCommand.PAUSE,
        "hold": OdinCommand.PAUSE,
        "stopp": OdinCommand.PAUSE,
        "pausar": OdinCommand.PAUSE,

        "resume": OdinCommand.RESUME,
        "back to normal": OdinCommand.RESUME,
        "weitermachen": OdinCommand.RESUME,
        "reanudar": OdinCommand.RESUME,
    }

    def __init__(
        self,
        handlers: dict[
            OdinCommand,
            Callable[[CommandRequest], Any],
        ]
        | None = None,
    ) -> None:
        self.handlers = handlers or {}
        self._history: list[CommandResult] = []

    def parse(
        self,
        text: str,
        chat_id: str,
    ) -> CommandRequest:
        """Convierte texto de Telegram en una solicitud de comando."""
        if not chat_id or not str(chat_id).strip():
            raise ValueError("chat_id cannot be empty")

        if not text or not text.strip():
            raise ValueError("text cannot be empty")

        normalized = self._normalize(text)

        command, argument = self._resolve_command(
            normalized
        )

        return CommandRequest(
            command=command,
            raw_text=text.strip(),
            chat_id=str(chat_id),
            argument=argument,
        )

    def handle(
        self,
        text: str,
        chat_id: str,
    ) -> CommandResult:
        """
        Interpreta y delega un comando.

        Un comando desconocido nunca ejecuta una acción.
        """
        request = self.parse(
            text=text,
            chat_id=chat_id,
        )

        if request.command == OdinCommand.UNKNOWN:
            result = CommandResult(
                command=OdinCommand.UNKNOWN,
                accepted=False,
                message="Unknown ODIN command",
            )

            self._history.append(result)
            return result

        handler = self.handlers.get(request.command)

        if handler is None:
            result = CommandResult(
                command=request.command,
                accepted=False,
                message="Command handler not configured",
            )

            self._history.append(result)
            return result

        try:
            data = handler(request)

            result = CommandResult(
                command=request.command,
                accepted=True,
                message="Command accepted",
                data=data,
            )

        except Exception as exc:
            result = CommandResult(
                command=request.command,
                accepted=False,
                message=str(exc),
            )

        self._history.append(result)
        return result

    def register_handler(
        self,
        command: OdinCommand,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Registra el ejecutor interno de un comando."""
        if command == OdinCommand.UNKNOWN:
            raise ValueError(
                "UNKNOWN command cannot have a handler"
            )

        if handler is None:
            raise ValueError("handler cannot be None")

        self.handlers[command] = handler

    def remove_handler(
        self,
        command: OdinCommand,
    ) -> bool:
        """Elimina un handler registrado."""
        if command not in self.handlers:
            return False

        del self.handlers[command]
        return True

    def supports(
        self,
        command: OdinCommand,
    ) -> bool:
        """Comprueba si existe un handler para el comando."""
        return command in self.handlers

    def get_history(self) -> list[CommandResult]:
        """Devuelve una copia del historial."""
        return list(self._history)

    def clear_history(self) -> None:
        """Limpia el historial en memoria."""
        self._history.clear()

    def count(self) -> int:
        """Cantidad de comandos procesados."""
        return len(self._history)

    def _resolve_command(
        self,
        normalized: str,
    ) -> tuple[OdinCommand, str | None]:
        """
        Resuelve el comando y conserva el resto como argumento.

        Ejemplo:

        'redo corregir el informe'

        se convierte en:

        REDO + 'corregir el informe'
        """
        if normalized.startswith("/"):
            normalized = normalized[1:].strip()

        if not normalized:
            return OdinCommand.UNKNOWN, None

        # Primero buscamos comandos compuestos.
        for name, command in sorted(
            self.COMMANDS.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            if normalized == name:
                return command, None

            prefix = f"{name} "

            if normalized.startswith(prefix):
                argument = normalized[len(prefix):].strip()

                return command, argument or None

        return OdinCommand.UNKNOWN, None

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(
            text.strip().lower().split()
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(handlers={len(self.handlers)}, "
            f"history={self.count()})"
  )

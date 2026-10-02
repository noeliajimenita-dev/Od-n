from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .odin_telegram_command_handler import (
    CommandRequest,
    CommandResult,
    OdinCommand,
    TelegramCommandHandler,
)


@dataclass(frozen=True)
class SupervisorCommandEvent:
    command: OdinCommand
    chat_id: str
    argument: str | None = None
    data: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command.value,
            "chat_id": self.chat_id,
            "argument": self.argument,
            "data": self.data,
        }


class TelegramCommandController:
    """
    Puente entre Telegram y el Supervisor.

    No ejecuta directamente operaciones externas peligrosas.
    Los handlers registrados determinan qué componente autorizado
    recibe cada comando.
    """

    def __init__(
        self,
        command_handler: TelegramCommandHandler | None = None,
    ) -> None:
        self.command_handler = (
            command_handler
            or TelegramCommandHandler()
        )

        self._events: list[SupervisorCommandEvent] = []

    def register(
        self,
        command: OdinCommand,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Registra la acción interna asociada a un comando."""
        self.command_handler.register_handler(
            command=command,
            handler=handler,
        )

    def handle(
        self,
        text: str,
        chat_id: str,
    ) -> CommandResult:
        """
        Procesa un comando y registra el evento resultante.
        """
        request = self.command_handler.parse(
            text=text,
            chat_id=chat_id,
        )

        result = self.command_handler.handle(
            text=text,
            chat_id=chat_id,
        )

        self._events.append(
            SupervisorCommandEvent(
                command=request.command,
                chat_id=request.chat_id,
                argument=request.argument,
                data=result.data,
            )
        )

        return result

    def approve(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Configura el handler de aprobación."""
        self.register(
            OdinCommand.APPROVE,
            handler,
        )

    def reject(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Configura el handler de rechazo."""
        self.register(
            OdinCommand.REJECT,
            handler,
        )

    def redo(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Configura el handler de corrección."""
        self.register(
            OdinCommand.REDO,
            handler,
        )

    def pause(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Configura el handler de pausa."""
        self.register(
            OdinCommand.PAUSE,
            handler,
        )

    def resume(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Configura el handler de reanudación."""
        self.register(
            OdinCommand.RESUME,
            handler,
        )

    def supported_commands(self) -> list[str]:
        """Lista los comandos que tienen handler configurado."""
        return [
            command.value
            for command in OdinCommand
            if command != OdinCommand.UNKNOWN
            and self.command_handler.supports(command)
        ]

    def get_events(self) -> list[SupervisorCommandEvent]:
        """Devuelve los eventos de comandos procesados."""
        return list(self._events)

    def get_last_event(
        self,
    ) -> SupervisorCommandEvent | None:
        """Obtiene el último evento procesado."""
        if not self._events:
            return None

        return self._events[-1]

    def clear_events(self) -> None:
        """Limpia el historial de eventos en memoria."""
        self._events.clear()

    def count_events(self) -> int:
        """Cantidad de comandos registrados."""
        return len(self._events)

    def status(self) -> dict[str, Any]:
        """Estado seguro del controlador."""
        return {
            "supported_commands": self.supported_commands(),
            "event_count": self.count_events(),
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(supported={len(self.supported_commands())}, "
            f"events={self.count_events()})"
    )

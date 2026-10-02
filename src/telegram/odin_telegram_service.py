from __future__ import annotations

from typing import Any, Callable

from .odin_telegram_client import TelegramClient, TelegramMessage
from .odin_telegram_command_controller import TelegramCommandController
from .odin_telegram_command_handler import CommandRequest, OdinCommand
from .odin_telegram_config import TelegramBotConfig
from .odin_telegram_message_router import TelegramMessageRouter
from .odin_telegram_response import TelegramResponseBuilder
from .odin_telegram_transport import TelegramHTTPTransport


class OdinTelegramService:
    """
    Servicio central de comunicación Telegram de ODIN.

    Flujo de entrada:

        Telegram
            ↓
        Transport
            ↓
        Client
            ↓
        Router
            ↓
        Command Controller / Message Handler
            ↓
        Supervisor

    Flujo de salida:

        Supervisor
            ↓
        Response Builder
            ↓
        Client
            ↓
        Telegram
    """

    def __init__(
        self,
        config: TelegramBotConfig,
        transport: TelegramHTTPTransport | None = None,
        command_controller: TelegramCommandController | None = None,
        router: TelegramMessageRouter | None = None,
        response_builder: TelegramResponseBuilder | None = None,
    ) -> None:
        if config is None:
            raise ValueError("config cannot be None")

        self.client = TelegramClient(
            config=config,
            transport=transport or TelegramHTTPTransport(),
        )

        self.command_controller = (
            command_controller
            or TelegramCommandController()
        )

        self.response_builder = (
            response_builder
            or TelegramResponseBuilder()
        )

        self.router = router or TelegramMessageRouter(
            command_handler=self._handle_command,
            message_handler=self._handle_message,
        )

        self._message_handler: Callable[
            [TelegramMessage],
            Any,
        ] | None = None

        self._running = False

    @property
    def bot_name(self) -> str:
        return self.client.bot_name

    @property
    def enabled(self) -> bool:
        return self.client.enabled

    def register_command(
        self,
        command: OdinCommand,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        """Registra una acción interna para un comando."""
        self.command_controller.register(
            command=command,
            handler=handler,
        )

    def register_approve_handler(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        self.command_controller.approve(handler)

    def register_reject_handler(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        self.command_controller.reject(handler)

    def register_redo_handler(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        self.command_controller.redo(handler)

    def register_pause_handler(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        self.command_controller.pause(handler)

    def register_resume_handler(
        self,
        handler: Callable[[CommandRequest], Any],
    ) -> None:
        self.command_controller.resume(handler)

    def register_message_handler(
        self,
        handler: Callable[[TelegramMessage], Any],
    ) -> None:
        """
        Registra el procesador de mensajes normales.

        Este handler normalmente será el Supervisor.
        """
        if handler is None:
            raise ValueError("handler cannot be None")

        self._message_handler = handler

    def poll_once(
        self,
        offset: int | None = None,
    ) -> list[Any]:
        """
        Realiza una iteración de recepción de Telegram.

        Devuelve los resultados producidos por los handlers.
        """
        if not self.enabled:
            return []

        messages = self.client.receive(
            offset=offset,
        )

        results: list[Any] = []

        for message in messages:
            result = self.router.dispatch(
                chat_id=message.chat_id,
                text=message.text,
            )

            results.append(result)

        return results

    def process_message(
        self,
        message: TelegramMessage,
    ) -> Any:
        """Procesa directamente un mensaje ya normalizado."""
        if message is None:
            raise ValueError("message cannot be None")

        return self.router.dispatch(
            chat_id=message.chat_id,
            text=message.text,
        )

    def send_text(
        self,
        text: str,
        chat_id: str | None = None,
    ) -> Any:
        """Envía texto directamente a Telegram."""
        return self.client.send(
            text=text,
            chat_id=chat_id,
        )

    def send_response(
        self,
        response: Any,
        chat_id: str | None = None,
    ) -> Any:
        """
        Envía una respuesta generada por ResponseBuilder.
        """
        telegram_response = (
            self.response_builder.from_result(response)
        )

        return self.client.send(
            text=telegram_response.text,
            chat_id=chat_id,
        )

    def send_status(
        self,
        status: str,
        details: dict[str, Any] | None = None,
        chat_id: str | None = None,
    ) -> Any:
        """Envía un estado seguro de ODIN."""
        response = self.response_builder.status(
            status=status,
            details=details,
        )

        return self.client.send(
            text=response.text,
            chat_id=chat_id,
        )

    def request_approval(
        self,
        action: str,
        reason: str,
        deadline_minutes: int | None = None,
        chat_id: str | None = None,
    ) -> Any:
        """
        Envía una solicitud de autorización al usuario.
        """
        response = self.response_builder.approval_required(
            action=action,
            reason=reason,
            deadline_minutes=deadline_minutes,
        )

        return self.client.send(
            text=response.text,
            chat_id=chat_id,
        )

    def start(self) -> None:
        """
        Marca el servicio como activo.

        El ciclo infinito de producción se deja al scheduler/runtime
        de ODIN para evitar bloquear el proceso principal.
        """
        self._running = True

    def stop(self) -> None:
        """Detiene el estado operativo del servicio."""
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def reset_updates(self) -> None:
        """Reinicia el cursor local de Telegram."""
        self.client.reset_offset()

    def supported_commands(self) -> list[str]:
        return self.command_controller.supported_commands()

    def status(self) -> dict[str, Any]:
        """
        Estado seguro y completo del canal Telegram.
        """
        return {
            "bot": self.client.safe_status(),
            "running": self._running,
            "supported_commands": self.supported_commands(),
            "routes": self.router.count_routes(),
            "command_events": (
                self.command_controller.count_events()
            ),
        }

    def _handle_command(
        self,
        text: str,
        chat_id: str,
    ) -> Any:
        result = self.command_controller.handle(
            text=text,
            chat_id=chat_id,
        )

        if not result.accepted:
            return self.response_builder.error(
                result.message,
                result.to_dict(),
            )

        return self.response_builder.success(
            result.message,
            result.to_dict(),
        )

    def _handle_message(
        self,
        text: str,
        chat_id: str,
    ) -> Any:
        """
        Entrega un mensaje normal al Supervisor.

        Si todavía no hay Supervisor conectado, devuelve una
        respuesta informativa en lugar de ejecutar nada.
        """
        if self._message_handler is None:
            return self.response_builder.info(
                "Mensaje recibido. Supervisor no conectado.",
            )

        message = TelegramMessage(
            update_id=-1,
            chat_id=chat_id,
            text=text,
            bot_name=self.bot_name,
        )

        try:
            result = self._message_handler(message)

            return self.response_builder.from_result(
                result,
            )

        except Exception as exc:
            return self.response_builder.error(
                f"Error procesando mensaje: {exc}",
            )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(bot_name={self.bot_name!r}, "
            f"running={self._running})"
      )

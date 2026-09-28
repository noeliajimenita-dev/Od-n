from collections.abc import Callable

from .command import TelegramCommand


class TelegramCommandRouter:
    def __init__(self):
        self.handlers: dict[str, Callable[[TelegramCommand], object]] = {}

    def register(
        self,
        command_name: str,
        handler: Callable[[TelegramCommand], object],
    ) -> None:
        command_name = command_name.strip().lower()

        if not command_name:
            raise ValueError("El nombre del comando no puede estar vacío.")

        self.handlers[command_name] = handler

    def dispatch(self, command: TelegramCommand):
        handler = self.handlers.get(command.name)

        if handler is None:
            raise KeyError(
                f"No existe un controlador para el comando: /{command.name}"
            )

        return handler(command)

    def has_handler(self, command_name: str) -> bool:
        return command_name.strip().lower() in self.handlers

    def get_commands(self) -> tuple[str, ...]:
        return tuple(sorted(self.handlers))

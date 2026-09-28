from .message import TelegramMessage


class TelegramMessageRouter:
    def __init__(self):
        self.routes: dict[str, str] = {}

    def register(self, bot_name: str, destination: str) -> None:
        if not bot_name.strip():
            raise ValueError("El nombre del bot no puede estar vacío.")

        if not destination.strip():
            raise ValueError("El destino no puede estar vacío.")

        self.routes[bot_name] = destination

    def route(self, message: TelegramMessage) -> str:
        if message.is_empty():
            raise ValueError("No se puede enrutar un mensaje vacío.")

        destination = self.routes.get(message.bot_name)

        if destination is None:
            raise KeyError(
                f"No existe una ruta para el bot: {message.bot_name}"
            )

        return destination

    def get_routes(self) -> dict[str, str]:
        return dict(self.routes)

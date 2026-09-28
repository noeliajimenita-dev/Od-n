from .connection_session import TelegramConnectionSession


class TelegramConnectionRegistry:
    def __init__(self):
        self.sessions: dict[str, TelegramConnectionSession] = {}

    def register(self, bot_name: str) -> TelegramConnectionSession:
        if not bot_name.strip():
            raise ValueError("El nombre del bot no puede estar vacío.")

        if bot_name in self.sessions:
            raise ValueError(f"El bot ya está registrado: {bot_name}")

        session = TelegramConnectionSession(bot_name=bot_name)
        self.sessions[bot_name] = session

        return session

    def get(self, bot_name: str) -> TelegramConnectionSession:
        if bot_name not in self.sessions:
            raise KeyError(f"Sesión no encontrada: {bot_name}")

        return self.sessions[bot_name]

    def get_all(self) -> dict[str, TelegramConnectionSession]:
        return dict(self.sessions)

    def remove(self, bot_name: str) -> None:
        if bot_name not in self.sessions:
            raise KeyError(f"Sesión no encontrada: {bot_name}")

        del self.sessions[bot_name]

    def count(self) -> int:
        return len(self.sessions)

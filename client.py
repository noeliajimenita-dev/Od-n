from dataclasses import dataclass

from .token_loader import load_bot_token


@dataclass
class TelegramClient:
    bot_name: str
    token_env_variable: str

    def get_token(self) -> str:
        """Carga el token del bot desde una variable de entorno."""
        return load_bot_token(self.token_env_variable)

    def is_ready(self) -> bool:
        """Comprueba si existe un token configurado."""
        try:
            self.get_token()
        except ValueError:
            return False

        return True

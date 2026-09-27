import os


def load_bot_token(env_variable: str) -> str:
    """
    Carga un token de Telegram desde una variable de entorno.

    El token nunca se almacena directamente en el código.
    """

    token = os.getenv(env_variable)

    if not token:
        raise ValueError(
            f"No se encontró el token requerido: {env_variable}"
        )

    return token

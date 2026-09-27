import os

from .settings import (
    APP_ENV,
    DAILY_TOKEN_LIMIT,
    MONTHLY_TOKEN_LIMIT,
    SAFETY_RESERVE_PERCENT,
)


def validate_configuration() -> list[str]:
    """
    Comprueba que la configuración básica sea válida.

    No requiere ni muestra las claves secretas.
    Devuelve una lista de errores encontrados.
    """

    errors = []

    # Entorno
    allowed_environments = {
        "development",
        "testing",
        "production",
    }

    if APP_ENV not in allowed_environments:
        errors.append(
            f"APP_ENV inválido: {APP_ENV}"
        )

    # Límites de recursos
    if DAILY_TOKEN_LIMIT < 0:
        errors.append(
            "DAILY_TOKEN_LIMIT no puede ser negativo."
        )

    if MONTHLY_TOKEN_LIMIT < 0:
        errors.append(
            "MONTHLY_TOKEN_LIMIT no puede ser negativo."
        )

    # Reserva de seguridad
    if not 0 <= SAFETY_RESERVE_PERCENT <= 100:
        errors.append(
            "SAFETY_RESERVE_PERCENT debe estar entre 0 y 100."
        )

    return errors


def configuration_is_valid() -> bool:
    """Devuelve True si no existen errores de configuración."""
    return len(validate_configuration()) == 0


if __name__ == "__main__":
    errors = validate_configuration()

    if errors:
        print("Configuración inválida:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Configuración válida.")

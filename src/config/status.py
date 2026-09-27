"""
Estado seguro de la configuración de THE ODIN PROJECT.

Este módulo nunca devuelve los valores de credenciales.
"""

from .security import get_missing_credentials
from .validation import validate_configuration
from .settings import APP_NAME, APP_ENV, APP_VERSION


def get_configuration_status() -> dict:
    """
    Devuelve un resumen seguro de la configuración.
    """

    errors = validate_configuration()
    missing_credentials = get_missing_credentials()

    return {
        "app_name": APP_NAME,
        "environment": APP_ENV,
        "version": APP_VERSION,
        "configuration_valid": len(errors) == 0,
        "configuration_errors": errors,
        "missing_credentials": missing_credentials,
    }


def is_ready_for_execution() -> bool:
    """
    Indica si la configuración básica es válida.

    La ausencia de credenciales no se considera un error
    durante la etapa inicial de desarrollo.
    """

    return len(validate_configuration()) == 0

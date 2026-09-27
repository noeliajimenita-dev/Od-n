"""
Punto de entrada para comprobar la configuración.
"""

from .status import get_configuration_status


def main() -> None:
    status = get_configuration_status()

    print(f"Proyecto: {status['app_name']}")
    print(f"Entorno: {status['environment']}")
    print(f"Versión: {status['version']}")
    print(
        f"Configuración válida: "
        f"{status['configuration_valid']}"
    )

    if status["configuration_errors"]:
        print("Errores de configuración:")

        for error in status["configuration_errors"]:
            print(f"- {error}")

    if status["missing_credentials"]:
        print(
            "Credenciales todavía no configuradas: "
            f"{len(status['missing_credentials'])}"
        )


if __name__ == "__main__":
    main()

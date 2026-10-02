from __future__ import annotations

from dataclasses import dataclass, field
import os


@dataclass(frozen=True)
class OdinDeploymentConfig:
    """
    Configuración de despliegue de ODIN.

    Los secretos nunca se almacenan en esta clase.
    Se obtienen exclusivamente desde variables de entorno
    o desde el gestor seguro de credenciales.
    """

    environment: str = "production"
    timezone: str = "America/Argentina/Buenos_Aires"

    host: str = "0.0.0.0"
    port: int = 8080

    work_directory: str = "/opt/odin"
    log_directory: str = "/opt/odin/logs"
    backup_directory: str = "/opt/odin/backups"

    restart_on_failure: bool = True
    run_24_7: bool = True

    required_environment_variables: tuple[str, ...] = field(
        default_factory=lambda: (
            "ODIN_ENVIRONMENT",
            "ODIN_TIMEZONE",
        )
    )

    @classmethod
    def from_environment(cls) -> "OdinDeploymentConfig":
        environment = os.getenv(
            "ODIN_ENVIRONMENT",
            "production",
        )

        timezone = os.getenv(
            "ODIN_TIMEZONE",
            "America/Argentina/Buenos_Aires",
        )

        host = os.getenv(
            "ODIN_HOST",
            "0.0.0.0",
        )

        port_value = os.getenv(
            "ODIN_PORT",
            "8080",
        )

        work_directory = os.getenv(
            "ODIN_WORK_DIRECTORY",
            "/opt/odin",
        )

        log_directory = os.getenv(
            "ODIN_LOG_DIRECTORY",
            f"{work_directory}/logs",
        )

        backup_directory = os.getenv(
            "ODIN_BACKUP_DIRECTORY",
            f"{work_directory}/backups",
        )

        restart_on_failure = cls._read_bool(
            "ODIN_RESTART_ON_FAILURE",
            True,
        )

        run_24_7 = cls._read_bool(
            "ODIN_RUN_24_7",
            True,
        )

        return cls(
            environment=environment,
            timezone=timezone,
            host=host,
            port=cls._read_port(port_value),
            work_directory=work_directory,
            log_directory=log_directory,
            backup_directory=backup_directory,
            restart_on_failure=restart_on_failure,
            run_24_7=run_24_7,
        )

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.environment:
            errors.append(
                "Deployment environment is empty"
            )

        if not self.timezone:
            errors.append(
                "Deployment timezone is empty"
            )

        if not self.host:
            errors.append(
                "Deployment host is empty"
            )

        if not 1 <= self.port <= 65535:
            errors.append(
                "Deployment port must be between 1 and 65535"
            )

        if not self.work_directory:
            errors.append(
                "Work directory is empty"
            )

        if not self.log_directory:
            errors.append(
                "Log directory is empty"
            )

        if not self.backup_directory:
            errors.append(
                "Backup directory is empty"
            )

        if not self.run_24_7:
            errors.append(
                "ODIN 24/7 execution is disabled"
            )

        return errors

    def is_valid(self) -> bool:
        return not self.validate()

    def to_dict(self) -> dict[str, object]:
        """
        Devuelve únicamente configuración no sensible.
        """

        return {
            "environment": self.environment,
            "timezone": self.timezone,
            "host": self.host,
            "port": self.port,
            "work_directory": self.work_directory,
            "log_directory": self.log_directory,
            "backup_directory": self.backup_directory,
            "restart_on_failure": self.restart_on_failure,
            "run_24_7": self.run_24_7,
        }

    @staticmethod
    def _read_bool(
        name: str,
        default: bool,
    ) -> bool:
        value = os.getenv(name)

        if value is None:
            return default

        normalized = value.strip().lower()

        if normalized in {
            "1",
            "true",
            "yes",
            "on",
        }:
            return True

        if normalized in {
            "0",
            "false",
            "no",
            "off",
        }:
            return False

        raise ValueError(
            f"Invalid boolean value for {name}"
        )

    @staticmethod
    def _read_port(value: str) -> int:
        try:
            port = int(value)
        except ValueError as exc:
            raise ValueError(
                "ODIN_PORT must be an integer"
            ) from exc

        if not 1 <= port <= 65535:
            raise ValueError(
                "ODIN_PORT must be between 1 and 65535"
            )

        return port

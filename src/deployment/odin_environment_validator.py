from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.deployment.odin_deployment_config import (
    OdinDeploymentConfig,
)


@dataclass
class EnvironmentValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


class OdinEnvironmentValidator:
    """
    Valida la configuración de producción de ODIN.

    No comprueba ni almacena secretos.
    Su responsabilidad es verificar que el entorno básico
    de despliegue sea coherente antes del arranque.
    """

    def validate(
        self,
        config: OdinDeploymentConfig,
    ) -> EnvironmentValidationResult:
        errors = list(config.validate())
        warnings: list[str] = []

        if config.environment.lower() != "production":
            warnings.append(
                "ODIN is not configured for production"
            )

        if not config.restart_on_failure:
            warnings.append(
                "Automatic restart after failure is disabled"
            )

        if config.host == "0.0.0.0":
            warnings.append(
                "ODIN is listening on all network interfaces"
            )

        return EnvironmentValidationResult(
            valid=not errors,
            errors=errors,
            warnings=warnings,
        )

    def is_valid(
        self,
        config: OdinDeploymentConfig,
    ) -> bool:
        return self.validate(config).valid

    def assert_valid(
        self,
        config: OdinDeploymentConfig,
    ) -> None:
        result = self.validate(config)

        if result.valid:
            return

        raise RuntimeError(
            "ODIN deployment validation failed: "
            + "; ".join(result.errors)
        )

    @staticmethod
    def validate_environment_variables(
        config: OdinDeploymentConfig,
    ) -> list[str]:
        """
        Devuelve las variables de entorno declaradas como
        requeridas pero ausentes.

        No devuelve valores de variables.
        """

        import os

        missing: list[str] = []

        for variable in config.required_environment_variables:
            if not os.getenv(variable):
                missing.append(variable)

        return missing

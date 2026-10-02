from __future__ import annotations

from typing import Any

from src.deployment.odin_deployment_config import (
    OdinDeploymentConfig,
)
from src.deployment.odin_environment_validator import (
    OdinEnvironmentValidator,
)
from src.integration.odin_system import OdinSystem
from src.integration.odin_system_validator import (
    OdinSystemValidator,
)


class OdinStartup:
    """
    Gestiona el arranque seguro de ODIN.

    El startup valida la infraestructura y el sistema
    antes de iniciar el runtime.
    """

    def __init__(
        self,
        system: OdinSystem,
        deployment_config: OdinDeploymentConfig | None = None,
        environment_validator: OdinEnvironmentValidator | None = None,
        system_validator: OdinSystemValidator | None = None,
    ) -> None:
        self.system = system

        self.deployment_config = (
            deployment_config
            or OdinDeploymentConfig.from_environment()
        )

        self.environment_validator = (
            environment_validator
            or OdinEnvironmentValidator()
        )

        self.system_validator = (
            system_validator
            or OdinSystemValidator()
        )

        self._started = False

    def validate(self) -> dict[str, Any]:
        deployment_result = (
            self.environment_validator.validate(
                self.deployment_config
            )
        )

        system_result = self.system_validator.validate(
            self.system
        )

        return {
            "valid": (
                deployment_result.valid
                and system_result.valid
            ),
            "deployment": deployment_result.to_dict(),
            "system": system_result.to_dict(),
        }

    def start(self) -> dict[str, Any]:
        validation = self.validate()

        if not validation["valid"]:
            raise RuntimeError(
                "ODIN startup validation failed"
            )

        self.system.start()
        self._started = True

        return self.status()

    def stop(self) -> dict[str, Any]:
        self.system.stop()
        self._started = False

        return self.status()

    def restart(self) -> dict[str, Any]:
        if self._started:
            self.stop()

        return self.start()

    def status(self) -> dict[str, Any]:
        return {
            "started": self._started,
            "deployment": self.deployment_config.to_dict(),
            "system": self.system.status(),
        }

    def startup_check(self) -> bool:
        validation = self.validate()
        return bool(validation["valid"])

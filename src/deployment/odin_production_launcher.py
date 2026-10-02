from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .odin_deployment_config import OdinDeploymentConfig
from .odin_environment_validator import OdinEnvironmentValidator
from .odin_startup import OdinStartup
from .odin_process_manager import OdinProcessManager


@dataclass
class OdinProductionStatus:
    valid: bool
    running: bool
    message: str


class OdinProductionLauncher:
    def __init__(
        self,
        system: Any,
        config: OdinDeploymentConfig | None = None,
    ) -> None:
        self.config = config or OdinDeploymentConfig.from_environment()

        self.environment_validator = OdinEnvironmentValidator()

        self.startup = OdinStartup(
            system=system,
            deployment_config=self.config,
            environment_validator=self.environment_validator,
        )

        self.process_manager = OdinProcessManager(
            startup=self.startup,
        )

    def validate(self) -> bool:
        result = self.startup.validate()
        return result.is_valid

    def start(self) -> bool:
        if not self.validate():
            return False

        return self.process_manager.start()

    def stop(self) -> bool:
        return self.process_manager.stop()

    def restart(self) -> bool:
        return self.process_manager.restart()

    def run_once(self) -> bool:
        if not self.process_manager.status().running:
            if not self.start():
                return False

        return self.process_manager.run_once()

    def run_forever(self) -> None:
        self.process_manager.run_forever()

    def status(self) -> OdinProductionStatus:
        process_status = self.process_manager.status()

        return OdinProductionStatus(
            valid=self.validate(),
            running=process_status.running,
            message=(
                "ODIN production runtime is active"
                if process_status.running
                else "ODIN production runtime is inactive"
            ),
        )


def create_launcher(system: Any) -> OdinProductionLauncher:
    return OdinProductionLauncher(system=system)


def main() -> None:
    """
    Punto de entrada para el servicio de producción.

    La construcción del sistema completo queda desacoplada
    para permitir que el integrador final inyecte la instancia
    real de OdinSystem.
    """
    raise RuntimeError(
        "Production launcher requires a configured OdinSystem "
        "integration before startup."
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

from src.deployment.odin_deployment_config import OdinDeploymentConfig
from src.deployment.odin_environment_validator import (
    OdinEnvironmentValidator,
)
from src.deployment.odin_process_manager import OdinProcessManager
from src.deployment.odin_service_manager import OdinServiceManager
from src.deployment.odin_startup import OdinStartup


class FakeSystem:
    def __init__(self) -> None:
        self.started = False
        self.stopped = False
        self.iterations = 0

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    def run_once(self) -> None:
        self.iterations += 1

    def status(self) -> dict[str, bool]:
        return {
            "started": self.started,
            "stopped": self.stopped,
        }


def valid_config() -> OdinDeploymentConfig:
    return OdinDeploymentConfig(
        environment="production",
        timezone="America/Argentina/Buenos_Aires",
        host="0.0.0.0",
        port=8080,
        work_directory="/opt/odin",
        log_directory="/opt/odin/logs",
        backup_directory="/opt/odin/backups",
        restart_on_failure=True,
        run_24_7=True,
    )


def test_deployment_config_is_valid() -> None:
    config = valid_config()

    assert config.validate() == []
    assert config.to_dict()["environment"] == "production"


def test_environment_validator_accepts_valid_config() -> None:
    config = valid_config()
    validator = OdinEnvironmentValidator()

    result = validator.validate(config)

    assert result.is_valid


def test_startup_starts_system() -> None:
    system = FakeSystem()
    startup = OdinStartup(
        system=system,
        deployment_config=valid_config(),
    )

    result = startup.start()

    assert result is True
    assert system.started is True


def test_process_manager_runs_iterations() -> None:
    system = FakeSystem()
    startup = OdinStartup(
        system=system,
        deployment_config=valid_config(),
    )

    manager = OdinProcessManager(
        startup=startup,
        interval_seconds=0,
        sleep_function=lambda _: None,
    )

    manager.run_forever(max_iterations=3)

    assert system.iterations == 3
    assert manager.status().iterations == 3
    assert manager.status().running is False


def test_process_manager_stops_system() -> None:
    system = FakeSystem()
    startup = OdinStartup(
        system=system,
        deployment_config=valid_config(),
    )

    manager = OdinProcessManager(
        startup=startup,
        interval_seconds=0,
        sleep_function=lambda _: None,
    )

    assert manager.start() is True
    assert manager.stop() is True
    assert system.stopped is True


def test_service_manager_start_stop() -> None:
    commands: list[list[str]] = []

    def runner(command: list[str]) -> int:
        commands.append(command)
        return 0

    manager = OdinServiceManager(
        service_name="odin",
        command_runner=runner,
    )

    assert manager.start() is True
    assert manager.enable() is True
    assert manager.stop() is True

    assert commands == [
        ["systemctl", "start", "odin"],
        ["systemctl", "enable", "odin"],
        ["systemctl", "stop", "odin"],
    ]


def test_service_manager_status() -> None:
    manager = OdinServiceManager(service_name="odin")

    assert manager.status().name == "odin"
    assert manager.status().active is False
    assert manager.status().enabled is False

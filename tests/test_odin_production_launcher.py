from __future__ import annotations

from src.deployment.odin_deployment_config import OdinDeploymentConfig
from src.deployment.odin_production_launcher import (
    OdinProductionLauncher,
)


class FakeSystem:
    def __init__(self) -> None:
        self.started = False
        self.stopped = False
        self.iterations = 0

    def start(self) -> None:
        self.started = True
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True
        self.started = False

    def run_once(self) -> None:
        self.iterations += 1

    def status(self) -> dict[str, bool]:
        return {
            "started": self.started,
            "stopped": self.stopped,
        }


def production_config() -> OdinDeploymentConfig:
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


def create_launcher() -> tuple[
    OdinProductionLauncher,
    FakeSystem,
]:
    system = FakeSystem()

    launcher = OdinProductionLauncher(
        system=system,
        config=production_config(),
    )

    launcher.process_manager.sleep_function = lambda _: None

    return launcher, system


def test_launcher_validates_configuration() -> None:
    launcher, _ = create_launcher()

    assert launcher.validate() is True


def test_launcher_starts_runtime() -> None:
    launcher, system = create_launcher()

    assert launcher.start() is True
    assert system.started is True
    assert launcher.status().running is True


def test_launcher_runs_single_iteration() -> None:
    launcher, system = create_launcher()

    assert launcher.run_once() is True
    assert system.iterations == 1


def test_launcher_stops_runtime() -> None:
    launcher, system = create_launcher()

    launcher.start()

    assert launcher.stop() is True
    assert system.stopped is True
    assert launcher.status().running is False


def test_launcher_restarts_runtime() -> None:
    launcher, system = create_launcher()

    launcher.start()

    assert launcher.restart() is True
    assert system.started is True
    assert launcher.status().running is True


def test_launcher_reports_production_status() -> None:
    launcher, _ = create_launcher()

    status = launcher.status()

    assert status.valid is True
    assert status.running is False
    assert "inactive" in status.message


def test_launcher_can_execute_multiple_iterations() -> None:
    launcher, system = create_launcher()

    launcher.process_manager.run_forever(max_iterations=3)

    assert system.iterations == 3
    assert launcher.process_manager.status().iterations == 3

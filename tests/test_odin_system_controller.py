from __future__ import annotations

from src.integration.odin_system import OdinSystem
from src.integration.odin_system_controller import OdinSystemController


class Runtime:
    def __init__(self) -> None:
        self.state = "stopped"

    def start(self) -> None:
        self.state = "running"

    def pause(self) -> None:
        self.state = "paused"

    def resume(self) -> None:
        self.state = "running"

    def stop(self) -> None:
        self.state = "stopped"

    def register_bot(self, schedule) -> None:
        pass

    def run_once(self, current_datetime=None):
        return {"executed": True}

    def status(self, current_datetime=None):
        return {"state": self.state}


class Logs:
    def summary(self):
        return {}

    def export(self):
        return {}


class Backups:
    def __init__(self) -> None:
        self.items = {}

    def create_backup(self, backup_id, version, data):
        backup = type(
            "Backup",
            (),
            {
                "to_dict": lambda self: {
                    "backup_id": backup_id,
                    "version": version,
                    "data": data,
                }
            },
        )()

        self.items[backup_id] = backup
        return backup

    def status(self):
        return {"count": len(self.items)}


class Recovery:
    def restore(self, backup_id):
        return type(
            "RecoveryResult",
            (),
            {
                "to_dict": lambda self: {
                    "success": True,
                    "backup_id": backup_id,
                }
            },
        )()

    def status(self):
        return {"state": "ready"}


class Execution:
    def execute(self, task):
        return {
            "success": True,
            "task": task,
        }


def build_controller() -> OdinSystemController:
    system = OdinSystem(
        runtime=Runtime(),
        logs=Logs(),
        backups=Backups(),
        recovery=Recovery(),
        execution_service=Execution(),
    )

    return OdinSystemController(system)


def test_controller_validation() -> None:
    controller = build_controller()

    result = controller.validate()

    assert result["valid"] is True


def test_controller_start() -> None:
    controller = build_controller()

    result = controller.start()

    assert result["success"] is True
    assert result["action"] == "start"
    assert result["status"]["started"] is True


def test_controller_pause_and_resume() -> None:
    controller = build_controller()

    controller.start()

    pause_result = controller.pause()

    assert pause_result["success"] is True
    assert (
        pause_result["status"]["runtime"]["state"]
        == "paused"
    )

    resume_result = controller.resume()

    assert resume_result["success"] is True
    assert (
        resume_result["status"]["runtime"]["state"]
        == "running"
    )


def test_controller_stop() -> None:
    controller = build_controller()

    controller.start()
    result = controller.stop()

    assert result["success"] is True
    assert result["action"] == "stop"
    assert result["status"]["started"] is False


def test_controller_run_once() -> None:
    controller = build_controller()

    result = controller.run_once()

    assert result["executed"] is True


def test_controller_execute_task() -> None:
    controller = build_controller()

    result = controller.execute_task("task-001")

    assert result["success"] is True
    assert result["task"] == "task-001"


def test_controller_create_backup() -> None:
    controller = build_controller()

    result = controller.create_backup(
        backup_id="backup-001",
        version="1.0.0",
        data={"state": "ok"},
    )

    assert result["backup_id"] == "backup-001"
    assert result["version"] == "1.0.0"


def test_controller_restore() -> None:
    controller = build_controller()

    result = controller.restore("backup-001")

    assert result["success"] is True
    assert result["backup_id"] == "backup-001"


def test_controller_register_bot() -> None:
    controller = build_controller()

    schedule = {
        "bot_id": "worker-1",
        "start": "04:00",
        "end": "22:10",
    }

    result = controller.register_bot(schedule)

    assert result["success"] is True
    assert result["action"] == "register_bot"


def test_controller_status() -> None:
    controller = build_controller()

    result = controller.status()

    assert result["started"] is False
    assert result["execution_configured"] is True


def test_invalid_system_is_rejected_before_start() -> None:
    system = OdinSystem(
        runtime=None,
        logs=None,
        backups=None,
        recovery=None,
    )

    controller = OdinSystemController(system)

    try:
        controller.start()
    except RuntimeError as exc:
        assert "validation failed" in str(exc).lower()
    else:
        raise AssertionError(
            "Expected invalid ODIN system to be rejected"
      )

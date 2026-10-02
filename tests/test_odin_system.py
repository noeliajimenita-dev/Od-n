from __future__ import annotations

from src.integration.odin_system import OdinSystem


class FakeRuntime:
    def __init__(self) -> None:
        self.started = False
        self.paused = False

    def start(self) -> None:
        self.started = True
        self.paused = False

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False

    def stop(self) -> None:
        self.started = False

    def register_bot(self, schedule) -> None:
        pass

    def run_once(self, current_datetime=None):
        return {"executed": True}

    def status(self, current_datetime=None):
        return {
            "started": self.started,
            "paused": self.paused,
        }


class FakeBackups:
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


class FakeRecovery:
    def __init__(self) -> None:
        self.restored = []

    def restore(self, backup_id):
        self.restored.append(backup_id)

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
        return {"restored": list(self.restored)}


class FakeLogs:
    pass


class FakeExecution:
    def execute(self, task):
        return {
            "task": task,
            "executed": True,
        }


def build_system() -> OdinSystem:
    return OdinSystem(
        runtime=FakeRuntime(),
        logs=FakeLogs(),
        backups=FakeBackups(),
        recovery=FakeRecovery(),
        execution_service=FakeExecution(),
    )


def test_system_start_pause_resume_stop() -> None:
    system = build_system()

    system.start()

    assert system._started is True
    assert system.runtime.started is True

    system.pause()

    assert system.runtime.paused is True

    system.resume()

    assert system.runtime.paused is False

    system.stop()

    assert system._started is False
    assert system.runtime.started is False


def test_system_run_once() -> None:
    system = build_system()

    result = system.run_once()

    assert result["executed"] is True


def test_system_execute_task() -> None:
    system = build_system()

    result = system.execute_task("task-001")

    assert result["executed"] is True
    assert result["task"] == "task-001"


def test_system_create_backup() -> None:
    system = build_system()

    result = system.create_backup(
        backup_id="backup-001",
        version="1.0.0",
        data={"state": "ok"},
    )

    assert result["backup_id"] == "backup-001"
    assert result["version"] == "1.0.0"


def test_system_restore() -> None:
    system = build_system()

    system.create_backup(
        backup_id="backup-001",
        version="1.0.0",
        data={"state": "ok"},
    )

    result = system.restore("backup-001")

    assert result["success"] is True
    assert result["backup_id"] == "backup-001"


def test_system_status() -> None:
    system = build_system()

    status = system.status()

    assert status["started"] is False
    assert status["execution_configured"] is True
    assert status["ai_configured"] is False

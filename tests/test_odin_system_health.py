from __future__ import annotations

from src.integration.odin_system import OdinSystem
from src.integration.odin_system_health import OdinSystemHealth


class HealthyRuntime:
    def status(self, current_datetime=None):
        return {"state": "running"}


class HealthyLogs:
    def status(self):
        return {"state": "available"}


class HealthyBackups:
    def status(self):
        return {"count": 1}


class HealthyRecovery:
    def status(self):
        return {"state": "ready"}


class ExecutionService:
    def execute(self, task):
        return {"success": True}


def build_system(
    execution: bool = True,
) -> OdinSystem:
    return OdinSystem(
        runtime=HealthyRuntime(),
        logs=HealthyLogs(),
        backups=HealthyBackups(),
        recovery=HealthyRecovery(),
        execution_service=(
            ExecutionService()
            if execution
            else None
        ),
    )


def test_healthy_system_is_healthy() -> None:
    health = OdinSystemHealth()
    system = build_system()

    result = health.check(system)

    assert result.healthy is True


def test_system_with_execution_is_ready() -> None:
    health = OdinSystemHealth()
    system = build_system(execution=True)

    result = health.check(system)

    assert result.healthy is True
    assert result.ready is True


def test_system_without_execution_is_not_ready() -> None:
    health = OdinSystemHealth()
    system = build_system(execution=False)

    result = health.check(system)

    assert result.healthy is True
    assert result.ready is False


def test_missing_runtime_is_unhealthy() -> None:
    health = OdinSystemHealth()

    system = build_system()
    system.runtime = None

    result = health.check(system)

    assert result.healthy is False
    assert result.ready is False

    runtime_check = next(
        check
        for check in result.checks
        if check.name == "runtime"
    )

    assert runtime_check.healthy is False


def test_missing_logs_is_unhealthy() -> None:
    health = OdinSystemHealth()

    system = build_system()
    system.logs = None

    result = health.check(system)

    assert result.healthy is False
    assert result.ready is False


def test_missing_backups_is_unhealthy() -> None:
    health = OdinSystemHealth()

    system = build_system()
    system.backups = None

    result = health.check(system)

    assert result.healthy is False


def test_missing_recovery_is_unhealthy() -> None:
    health = OdinSystemHealth()

    system = build_system()
    system.recovery = None

    result = health.check(system)

    assert result.healthy is False


def test_optional_ai_component_can_be_missing() -> None:
    health = OdinSystemHealth()
    system = build_system()

    system.ai_service = None

    result = health.check(system)

    assert result.healthy is True

    ai_check = next(
        check
        for check in result.checks
        if check.name == "ai_service"
    )

    assert ai_check.healthy is False
    assert "optional" in ai_check.details.lower()


def test_optional_platform_manager_can_be_missing() -> None:
    health = OdinSystemHealth()
    system = build_system()

    result = health.check(system)

    platform_check = next(
        check
        for check in result.checks
        if check.name == "platform_manager"
    )

    assert platform_check.healthy is False


def test_is_healthy_returns_boolean() -> None:
    health = OdinSystemHealth()
    system = build_system()

    assert health.is_healthy(system) is True


def test_is_ready_returns_boolean() -> None:
    health = OdinSystemHealth()
    system = build_system()

    assert health.is_ready(system) is True


def test_none_system_is_not_healthy() -> None:
    health = OdinSystemHealth()

    result = health.check(None)

    assert result.healthy is False
    assert result.ready is False
    assert result.checks[0].name == "system"


def test_status_exception_marks_component_unhealthy() -> None:
    class BrokenRuntime:
        def status(self, current_datetime=None):
            raise RuntimeError("runtime failure")

    system = build_system()
    system.runtime = BrokenRuntime()

    health = OdinSystemHealth()
    result = health.check(system)

    assert result.healthy is False

    runtime_check = next(
        check
        for check in result.checks
        if check.name == "runtime"
    )

    assert runtime_check.healthy is False
    assert "failed" in runtime_check.details.lower()

from __future__ import annotations

from src.integration.odin_system import OdinSystem
from src.integration.odin_system_validator import OdinSystemValidator


class ValidRuntime:
    def start(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def run_once(self, current_datetime=None):
        return {}

    def status(self, current_datetime=None):
        return {}


class ValidLogs:
    def summary(self):
        return {}

    def export(self):
        return {}


class ValidBackups:
    def create_backup(self, backup_id, version, data):
        return None

    def status(self):
        return {}


class ValidRecovery:
    def restore(self, backup_id):
        return None

    def status(self):
        return {}


def build_valid_system() -> OdinSystem:
    return OdinSystem(
        runtime=ValidRuntime(),
        logs=ValidLogs(),
        backups=ValidBackups(),
        recovery=ValidRecovery(),
    )


def test_valid_system_passes_validation() -> None:
    validator = OdinSystemValidator()
    system = build_valid_system()

    result = validator.validate(system)

    assert result.valid is True
    assert result.errors == []


def test_missing_runtime_is_detected() -> None:
    validator = OdinSystemValidator()

    system = OdinSystem(
        runtime=None,
        logs=ValidLogs(),
        backups=ValidBackups(),
        recovery=ValidRecovery(),
    )

    result = validator.validate(system)

    assert result.valid is False
    assert any(
        "runtime" in error
        for error in result.errors
    )


def test_missing_logs_is_detected() -> None:
    validator = OdinSystemValidator()

    system = OdinSystem(
        runtime=ValidRuntime(),
        logs=None,
        backups=ValidBackups(),
        recovery=ValidRecovery(),
    )

    result = validator.validate(system)

    assert result.valid is False
    assert any(
        "logs" in error
        for error in result.errors
    )


def test_missing_backup_manager_is_detected() -> None:
    validator = OdinSystemValidator()

    system = OdinSystem(
        runtime=ValidRuntime(),
        logs=ValidLogs(),
        backups=None,
        recovery=ValidRecovery(),
    )

    result = validator.validate(system)

    assert result.valid is False
    assert any(
        "backups" in error
        for error in result.errors
    )


def test_missing_recovery_manager_is_detected() -> None:
    validator = OdinSystemValidator()

    system = OdinSystem(
        runtime=ValidRuntime(),
        logs=ValidLogs(),
        backups=ValidBackups(),
        recovery=None,
    )

    result = validator.validate(system)

    assert result.valid is False
    assert any(
        "recovery" in error
        for error in result.errors
    )


def test_optional_components_generate_warnings() -> None:
    validator = OdinSystemValidator()
    system = build_valid_system()

    result = validator.validate(system)

    assert result.valid is True
    assert len(result.warnings) >= 1

    assert any(
        "execution_service" in warning
        for warning in result.warnings
    )


def test_missing_required_method_is_detected() -> None:
    class InvalidRuntime:
        def start(self):
            pass

    system = OdinSystem(
        runtime=InvalidRuntime(),
        logs=ValidLogs(),
        backups=ValidBackups(),
        recovery=ValidRecovery(),
    )

    validator = OdinSystemValidator()
    result = validator.validate(system)

    assert result.valid is False

    assert any(
        "runtime" in error
        and "pause" in error
        for error in result.errors
    )


def test_is_valid_returns_boolean() -> None:
    validator = OdinSystemValidator()
    system = build_valid_system()

    assert validator.is_valid(system) is True


def test_assert_valid_accepts_valid_system() -> None:
    validator = OdinSystemValidator()
    system = build_valid_system()

    validator.assert_valid(system)


def test_assert_valid_rejects_invalid_system() -> None:
    validator = OdinSystemValidator()

    system = OdinSystem(
        runtime=None,
        logs=None,
        backups=None,
        recovery=None,
    )

    try:
        validator.assert_valid(system)
    except RuntimeError as exc:
        assert "validation failed" in str(exc).lower()
    else:
        raise AssertionError(
            "Expected RuntimeError for invalid ODIN system"
)

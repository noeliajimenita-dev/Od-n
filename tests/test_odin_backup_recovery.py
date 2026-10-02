from datetime import datetime

import pytest

from src.runtime.odin_backup import (
    OdinBackup,
    OdinBackupManager,
)
from src.runtime.odin_recovery import (
    OdinRecoveryManager,
)


def test_backup_can_be_created():
    manager = OdinBackupManager()

    backup = manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
        data={"status": "stable"},
    )

    assert isinstance(
        backup,
        OdinBackup,
    )
    assert backup.backup_id == "backup_001"
    assert backup.version == "1.0.0"
    assert backup.data["status"] == "stable"


def test_latest_backup_is_protected():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
    )

    latest = manager.latest()

    assert latest is not None
    assert latest.protected is True


def test_second_backup_becomes_latest():
    manager = OdinBackupManager()

    first = manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
    )

    second = manager.create_backup(
        backup_id="backup_002",
        version="1.1.0",
    )

    assert manager.latest() == second
    assert second.protected is True
    assert first.protected is False


def test_backup_can_be_found_by_version():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
    )

    backup = manager.get_by_version(
        "1.0.0"
    )

    assert backup is not None
    assert backup.backup_id == "backup_001"


def test_backup_data_can_be_restored():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
        data={
            "workers": 5,
            "runtime": "stable",
        },
    )

    data = manager.restore_data(
        "backup_001"
    )

    assert data["workers"] == 5
    assert data["runtime"] == "stable"


def test_protected_backup_cannot_be_deleted():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
    )

    with pytest.raises(PermissionError):
        manager.delete("backup_001")


def test_system_cannot_delete_last_backup():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
    )

    manager.unprotect = (
        lambda backup_id: None
    )

    backup = manager.get("backup_001")
    assert backup is not None

    backup.protected = False

    with pytest.raises(PermissionError):
        manager.delete("backup_001")


def test_non_latest_backup_can_be_deleted():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
    )

    manager.create_backup(
        backup_id="backup_002",
        version="1.1.0",
    )

    assert manager.delete(
        "backup_001"
    ) is True

    assert not manager.has_backup(
        "backup_001"
    )

    assert manager.has_backup(
        "backup_002"
    )


def test_recovery_restores_backup():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
        data={
            "runtime": "stable",
        },
    )

    restored_data = []

    recovery = OdinRecoveryManager(
        backup_manager=manager,
        restore_callback=lambda data: (
            restored_data.append(data)
        ),
    )

    result = recovery.restore(
        "backup_001"
    )

    assert result.successful
    assert result.status == "restored"
    assert result.version == "1.0.0"
    assert restored_data[0]["runtime"] == "stable"


def test_recovery_can_use_version():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="2.0.0",
        data={
            "version": "2.0.0",
        },
    )

    recovery = OdinRecoveryManager(
        backup_manager=manager
    )

    result = recovery.restore_version(
        "2.0.0"
    )

    assert result.successful
    assert result.version == "2.0.0"


def test_recovery_fails_for_missing_backup():
    manager = OdinBackupManager()

    recovery = OdinRecoveryManager(
        backup_manager=manager
    )

    result = recovery.restore(
        "missing"
    )

    assert not result.successful
    assert result.status == "failed"
    assert result.error == "Backup not found"


def test_recovery_fails_for_missing_version():
    manager = OdinBackupManager()

    recovery = OdinRecoveryManager(
        backup_manager=manager
    )

    result = recovery.restore_version(
        "99.0.0"
    )

    assert not result.successful
    assert result.status == "failed"
    assert result.error == "Version not found"


def test_recovery_records_history():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
        data={"state": "ok"},
    )

    recovery = OdinRecoveryManager(
        backup_manager=manager
    )

    recovery.restore(
        "backup_001"
    )

    history = recovery.get_history()

    assert len(history) == 1
    assert history[0].backup_id == "backup_001"


def test_recovery_callback_errors_are_captured():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
        data={"state": "ok"},
    )

    def failing_restore(data):
        raise RuntimeError(
            "Restore failed"
        )

    recovery = OdinRecoveryManager(
        backup_manager=manager,
        restore_callback=failing_restore,
    )

    result = recovery.restore(
        "backup_001"
    )

    assert not result.successful
    assert result.status == "failed"
    assert result.error == "Restore failed"


def test_backup_status_reports_protected_backups():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
    )

    status = manager.status()

    assert status["total_backups"] == 1
    assert status["latest_backup"] == "backup_001"
    assert "backup_001" in (
        status["protected_backups"]
    )


def test_recovery_status_reports_last_operation():
    manager = OdinBackupManager()

    manager.create_backup(
        backup_id="backup_001",
        version="1.0.0",
        data={"state": "stable"},
    )

    recovery = OdinRecoveryManager(
        backup_manager=manager
    )

    recovery.restore(
        "backup_001"
    )

    status = recovery.status()

    assert status["recoveries"] == 1
    assert (
        status["latest_backup_id"]
        == "backup_001"
    )
    assert (
        status["last_recovery"]["status"]
        == "restored"
  )

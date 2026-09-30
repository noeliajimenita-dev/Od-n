import pytest

from src.worker_1.status import (
    Worker1Status,
    Worker1StatusManager,
)


def test_default_status_is_idle():
    manager = Worker1StatusManager()

    assert manager.status == Worker1Status.IDLE


def test_set_working_status():
    manager = Worker1StatusManager()

    manager.set_status(Worker1Status.WORKING)

    assert manager.status == Worker1Status.WORKING
    assert manager.is_working() is True


def test_set_paused_status():
    manager = Worker1StatusManager()

    manager.set_status(Worker1Status.PAUSED)

    assert manager.status == Worker1Status.PAUSED
    assert manager.is_paused() is True


def test_set_stopped_status():
    manager = Worker1StatusManager()

    manager.set_status(Worker1Status.STOPPED)

    assert manager.status == Worker1Status.STOPPED
    assert manager.is_stopped() is True


def test_idle_status_is_available():
    manager = Worker1StatusManager()

    assert manager.is_available() is True


def test_working_status_is_not_available():
    manager = Worker1StatusManager()

    manager.set_status(Worker1Status.WORKING)

    assert manager.is_available() is False


def test_invalid_status_fails():
    manager = Worker1StatusManager()

    with pytest.raises(ValueError):
        manager.set_status("invalid_status")


def test_status_can_return_to_idle():
    manager = Worker1StatusManager()

    manager.set_status(Worker1Status.WORKING)
    manager.set_status(Worker1Status.IDLE)

    assert manager.status == Worker1Status.IDLE
    assert manager.is_available() is True

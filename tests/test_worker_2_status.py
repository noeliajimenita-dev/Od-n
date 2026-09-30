import pytest

from src.worker_2.status import (
    Worker2Status,
    Worker2StatusManager,
)


def test_default_status_is_idle():
    manager = Worker2StatusManager()

    assert manager.status == Worker2Status.IDLE


def test_set_working_status():
    manager = Worker2StatusManager()

    manager.set_status(Worker2Status.WORKING)

    assert manager.status == Worker2Status.WORKING
    assert manager.is_working() is True


def test_set_paused_status():
    manager = Worker2StatusManager()

    manager.set_status(Worker2Status.PAUSED)

    assert manager.status == Worker2Status.PAUSED
    assert manager.is_paused() is True


def test_set_stopped_status():
    manager = Worker2StatusManager()

    manager.set_status(Worker2Status.STOPPED)

    assert manager.status == Worker2Status.STOPPED
    assert manager.is_stopped() is True


def test_idle_status_is_available():
    manager = Worker2StatusManager()

    assert manager.is_available() is True


def test_working_status_is_not_available():
    manager = Worker2StatusManager()

    manager.set_status(Worker2Status.WORKING)

    assert manager.is_available() is False


def test_invalid_status_fails():
    manager = Worker2StatusManager()

    with pytest.raises(ValueError):
        manager.set_status("invalid_status")


def test_status_can_return_to_idle():
    manager = Worker2StatusManager()

    manager.set_status(Worker2Status.WORKING)
    manager.set_status(Worker2Status.IDLE)

    assert manager.status == Worker2Status.IDLE
    assert manager.is_available() is True

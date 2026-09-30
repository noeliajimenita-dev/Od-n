import pytest

from src.worker_3.status import Worker3Status, Worker3StatusManager


def test_default_status_is_idle():
    manager = Worker3StatusManager()

    assert manager.status == Worker3Status.IDLE


def test_set_working_status():
    manager = Worker3StatusManager()

    manager.set_status(Worker3Status.WORKING)

    assert manager.status == Worker3Status.WORKING
    assert manager.is_working() is True


def test_set_paused_status():
    manager = Worker3StatusManager()

    manager.set_status(Worker3Status.PAUSED)

    assert manager.status == Worker3Status.PAUSED
    assert manager.is_paused() is True


def test_set_stopped_status():
    manager = Worker3StatusManager()

    manager.set_status(Worker3Status.STOPPED)

    assert manager.status == Worker3Status.STOPPED
    assert manager.is_stopped() is True


def test_idle_worker_is_available():
    manager = Worker3StatusManager()

    assert manager.is_available() is True


def test_working_worker_is_not_available():
    manager = Worker3StatusManager()

    manager.set_status(Worker3Status.WORKING)

    assert manager.is_available() is False


def test_paused_worker_is_not_available():
    manager = Worker3StatusManager()

    manager.set_status(Worker3Status.PAUSED)

    assert manager.is_available() is False


def test_stopped_worker_is_not_available():
    manager = Worker3StatusManager()

    manager.set_status(Worker3Status.STOPPED)

    assert manager.is_available() is False


def test_invalid_status_fails():
    manager = Worker3StatusManager()

    with pytest.raises(ValueError):
        manager.set_status("invalid")


def test_status_can_return_to_idle():
    manager = Worker3StatusManager()

    manager.set_status(Worker3Status.WORKING)
    manager.set_status(Worker3Status.IDLE)

    assert manager.status == Worker3Status.IDLE
    assert manager.is_available() is True

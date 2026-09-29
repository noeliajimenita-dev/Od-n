from src.telegram.connection_supervisor import TelegramConnectionSupervisor
from src.telegram.connection_supervisor_status import (
    get_connection_supervisor_status,
)


class FakeService:
    def __init__(self):
        self._controllers = {
            "bot_1": type("Controller", (), {"session": type("Session", (), {"connected": True})()})(),
            "bot_2": type("Controller", (), {"session": type("Session", (), {"connected": False})()})(),
        }

    def get_all_controllers(self):
        return self._controllers


def test_connection_supervisor_status_counts_bots():
    supervisor = TelegramConnectionSupervisor(FakeService())

    status = get_connection_supervisor_status(supervisor)

    assert status.total_bots == 2
    assert status.connected_bots == 1
    assert status.disconnected_bots == 1
    assert status.all_connected is False

from src.telegram.connection_supervisor import TelegramConnectionSupervisor
from src.telegram.connection_supervisor_report import (
    build_connection_supervisor_report,
)


class FakeSession:
    def __init__(self, connected: bool):
        self.connected = connected


class FakeController:
    def __init__(self, connected: bool):
        self.session = FakeSession(connected)


class FakeService:
    def __init__(self):
        self._controllers = {
            "bot_1": FakeController(True),
            "bot_2": FakeController(False),
        }

    def get_all_controllers(self):
        return self._controllers


def test_connection_supervisor_report():
    supervisor = TelegramConnectionSupervisor(FakeService())

    report = build_connection_supervisor_report(supervisor)

    assert "TELEGRAM CONNECTION SUPERVISOR" in report
    assert "Total bots: 2" in report
    assert "Connected: 1" in report
    assert "Disconnected: 1" in report
    assert "Global status: CONNECTION_ISSUES" in report
    assert "bot_1" in report
    assert "bot_2" in report

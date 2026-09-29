from src.telegram.connection_supervisor import TelegramConnectionSupervisor
from src.telegram.connection_supervisor_controller import (
    TelegramConnectionSupervisorController,
)


class FakeSession:
    def __init__(self, connected: bool = False):
        self.connected = connected


class FakeController:
    def __init__(self):
        self.session = FakeSession()

    def connect(self):
        self.session.connected = True

    def disconnect(self):
        self.session.connected = False


class FakeService:
    def __init__(self):
        self._controllers = {
            "bot_1": FakeController(),
            "bot_2": FakeController(),
        }

    def get_all_controllers(self):
        return self._controllers

    def connect(self, bot_name: str):
        self._controllers[bot_name].connect()

    def disconnect(self, bot_name: str):
        self._controllers[bot_name].disconnect()

    def recover(self, bot_name: str):
        if not self._controllers[bot_name].session.connected:
            self._controllers[bot_name].connect()


def test_controller_connects_bot():
    service = FakeService()
    supervisor = TelegramConnectionSupervisor(service)
    controller = TelegramConnectionSupervisorController(supervisor)

    controller.connect_bot("bot_1")

    assert "bot_1" in controller.get_connected_bots()


def test_controller_disconnects_bot():
    service = FakeService()
    supervisor = TelegramConnectionSupervisor(service)
    controller = TelegramConnectionSupervisorController(supervisor)

    controller.connect_bot("bot_1")
    controller.disconnect_bot("bot_1")

    assert "bot_1" in controller.get_disconnected_bots()


def test_controller_recovers_bot():
    service = FakeService()
    supervisor = TelegramConnectionSupervisor(service)
    controller = TelegramConnectionSupervisorController(supervisor)

    controller.recover_bot("bot_1")

    assert "bot_1" in controller.get_connected_bots()

from src.telegram.connection_supervisor import TelegramConnectionSupervisor
from src.telegram.connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)
from src.telegram.connection_supervisor_controller import (
    TelegramConnectionSupervisorController,
)
from src.telegram.connection_supervisor_command_handler import (
    TelegramConnectionSupervisorCommandHandler,
)


class FakeSession:
    def __init__(self, connected=False):
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

    def connect(self, bot_name):
        self._controllers[bot_name].connect()

    def disconnect(self, bot_name):
        self._controllers[bot_name].disconnect()

    def recover(self, bot_name):
        if not self._controllers[bot_name].session.connected:
            self._controllers[bot_name].connect()


def create_handler():
    service = FakeService()
    supervisor = TelegramConnectionSupervisor(service)
    controller = TelegramConnectionSupervisorController(supervisor)
    return TelegramConnectionSupervisorCommandHandler(controller)


def test_handle_connect():
    handler = create_handler()

    result = handler.handle(
        ConnectionCommandRequest(
            command=ConnectionCommand.CONNECT,
            bot_name="bot_1",
        )
    )

    assert result == "Bot conectado: bot_1"


def test_handle_disconnect():
    handler = create_handler()

    handler.handle(
        ConnectionCommandRequest(
            command=ConnectionCommand.CONNECT,
            bot_name="bot_1",
        )
    )

    result = handler.handle(
        ConnectionCommandRequest(
            command=ConnectionCommand.DISCONNECT,
            bot_name="bot_1",
        )
    )

    assert result == "Bot desconectado: bot_1"


def test_handle_recover():
    handler = create_handler()

    result = handler.handle(
        ConnectionCommandRequest(
            command=ConnectionCommand.RECOVER,
            bot_name="bot_1",
        )
    )

    assert result == "Bot recuperado: bot_1"


def test_handle_status():
    handler = create_handler()

    result = handler.handle(
        ConnectionCommandRequest(
            command=ConnectionCommand.STATUS,
        )
    )

    assert "Conectados: 0" in result
    assert "Desconectados: 2" in result

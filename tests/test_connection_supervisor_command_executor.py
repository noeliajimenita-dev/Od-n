from src.telegram.connection_supervisor import TelegramConnectionSupervisor
from src.telegram.connection_supervisor_command_executor import (
    TelegramConnectionSupervisorCommandExecutor,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)
from src.telegram.connection_supervisor_controller import (
    TelegramConnectionSupervisorController,
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


def create_executor():
    service = FakeService()
    supervisor = TelegramConnectionSupervisor(service)
    controller = TelegramConnectionSupervisorController(supervisor)
    return TelegramConnectionSupervisorCommandExecutor(controller)


def test_execute_connect():
    executor = create_executor()

    result = executor.execute(
        ConnectionCommandRequest(
            command=ConnectionCommand.CONNECT,
            bot_name="bot_1",
        )
    )

    assert result.success is True
    assert result.bot_name == "bot_1"


def test_execute_disconnect():
    executor = create_executor()

    executor.execute(
        ConnectionCommandRequest(
            command=ConnectionCommand.CONNECT,
            bot_name="bot_1",
        )
    )

    result = executor.execute(
        ConnectionCommandRequest(
            command=ConnectionCommand.DISCONNECT,
            bot_name="bot_1",
        )
    )

    assert result.success is True
    assert result.bot_name == "bot_1"


def test_execute_recover():
    executor = create_executor()

    result = executor.execute(
        ConnectionCommandRequest(
            command=ConnectionCommand.RECOVER,
            bot_name="bot_1",
        )
    )

    assert result.success is True
    assert result.bot_name == "bot_1"


def test_execute_status():
    executor = create_executor()

    result = executor.execute(
        ConnectionCommandRequest(
            command=ConnectionCommand.STATUS,
        )
    )

    assert result.success is True
    assert "Conectados: 0" in result.message
    assert "Desconectados: 2" in result.message


def test_execute_requires_bot():
    executor = create_executor()

    result = executor.execute(
        ConnectionCommandRequest(
            command=ConnectionCommand.CONNECT,
        )
    )

    assert result.success is False
    assert "requiere un bot" in result.message

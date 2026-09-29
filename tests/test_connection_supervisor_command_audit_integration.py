from src.telegram.connection_supervisor import TelegramConnectionSupervisor
from src.telegram.connection_supervisor_command_audit_integration import (
    ConnectionSupervisorCommandAuditIntegration,
)
from src.telegram.connection_supervisor_command_audit_service import (
    ConnectionCommandAuditService,
)
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


def create_integration():
    service = FakeService()

    supervisor = TelegramConnectionSupervisor(service)

    controller = TelegramConnectionSupervisorController(
        supervisor
    )

    executor = TelegramConnectionSupervisorCommandExecutor(
        controller
    )

    audit_service = ConnectionCommandAuditService()

    integration = ConnectionSupervisorCommandAuditIntegration(
        executor=executor,
        audit_service=audit_service,
    )

    return integration, audit_service


def test_command_execution_is_audited():
    integration, audit_service = create_integration()

    request = ConnectionCommandRequest(
        command=ConnectionCommand.CONNECT,
        bot_name="bot_1",
    )

    result = integration.execute(request)

    assert result.success is True
    assert audit_service.count() == 1

    audit = audit_service.get_all()[0]

    assert audit.command == "CONNECT"
    assert audit.bot_name == "bot_1"
    assert audit.success is True


def test_failed_command_is_also_audited():
    integration, audit_service = create_integration()

    request = ConnectionCommandRequest(
        command=ConnectionCommand.CONNECT,
    )

    result = integration.execute(request)

    assert result.success is False
    assert audit_service.count() == 1

    audit = audit_service.get_all()[0]

    assert audit.command == "CONNECT"
    assert audit.success is False

from src.telegram.connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)
from src.telegram.connection_supervisor_command_message_factory import (
    ConnectionSupervisorCommandMessageFactory,
)
from src.telegram.connection_supervisor_command_message_service import (
    ConnectionSupervisorCommandMessageService,
)
from src.telegram.connection_supervisor_command_message_controller import (
    ConnectionSupervisorCommandMessageController,
)
from src.telegram.connection_supervisor_command_message_integration import (
    ConnectionSupervisorCommandMessageIntegration,
)


class FakeParser:
    def parse(self, message: str) -> str | None:
        commands = {
            "approved": "APPROVE",
            "rejected": "REJECT",
            "redo": "REDO",
            "pause": "PAUSE",
            "resume": "RESUME",
        }

        return commands.get(message.strip().lower())


def build_integration():
    parser = FakeParser()

    factory = ConnectionSupervisorCommandMessageFactory(parser)
    service = ConnectionSupervisorCommandMessageService(factory)
    controller = ConnectionSupervisorCommandMessageController(service)

    return ConnectionSupervisorCommandMessageIntegration(controller)


def test_complete_command_flow():
    integration = build_integration()

    result = integration.receive("Approved")

    assert isinstance(result, ConnectionSupervisorCommandMessage)
    assert result.raw_text == "Approved"
    assert result.command == "APPROVE"
    assert result.is_valid is True


def test_complete_invalid_command_flow():
    integration = build_integration()

    result = integration.receive("unknown command")

    assert isinstance(result, ConnectionSupervisorCommandMessage)
    assert result.raw_text == "unknown command"
    assert result.command is None
    assert result.is_valid is False


def test_complete_validity_check():
    integration = build_integration()

    assert integration.accepts("Approved") is True
    assert integration.accepts("Rejected") is True
    assert integration.accepts("Redo") is True
    assert integration.accepts("Pause") is True
    assert integration.accepts("Resume") is True
    assert integration.accepts("unknown command") is False

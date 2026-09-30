from src.telegram.connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)
from src.telegram.connection_supervisor_command_message_integration import (
    ConnectionSupervisorCommandMessageIntegration,
)


class FakeController:
    def __init__(self, message):
        self.message = message

    def handle(self, raw_text: str):
        return self.message

    def is_valid(self, raw_text: str) -> bool:
        return self.message.is_valid


def test_integration_receives_valid_command():
    message = ConnectionSupervisorCommandMessage(
        raw_text="Approved",
        command="APPROVE",
    )

    controller = FakeController(message)
    integration = ConnectionSupervisorCommandMessageIntegration(controller)

    result = integration.receive("Approved")

    assert result.raw_text == "Approved"
    assert result.command == "APPROVE"
    assert result.is_valid is True


def test_integration_accepts_valid_command():
    message = ConnectionSupervisorCommandMessage(
        raw_text="Approved",
        command="APPROVE",
    )

    controller = FakeController(message)
    integration = ConnectionSupervisorCommandMessageIntegration(controller)

    assert integration.accepts("Approved") is True


def test_integration_rejects_invalid_command():
    message = ConnectionSupervisorCommandMessage(
        raw_text="unknown",
        command=None,
    )

    controller = FakeController(message)
    integration = ConnectionSupervisorCommandMessageIntegration(controller)

    assert integration.accepts("unknown") is False

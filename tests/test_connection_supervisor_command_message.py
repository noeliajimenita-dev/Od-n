from src.telegram.connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)


def test_valid_command_message():
    message = ConnectionSupervisorCommandMessage(
        raw_text="Approved",
        command="APPROVE",
    )

    assert message.raw_text == "Approved"
    assert message.command == "APPROVE"
    assert message.is_valid is True


def test_invalid_command_message():
    message = ConnectionSupervisorCommandMessage(
        raw_text="something unknown",
        command=None,
    )

    assert message.is_valid is False

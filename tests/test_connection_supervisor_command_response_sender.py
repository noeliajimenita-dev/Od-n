from unittest.mock import Mock

from src.telegram.connection_supervisor_command_response_sender import (
    ConnectionSupervisorCommandResponseSender,
)


def test_send_forwards_response_to_sender():
    sender = Mock()

    response_sender = ConnectionSupervisorCommandResponseSender(
        sender
    )

    response_sender.send("COMMAND_OK")

    sender.assert_called_once_with("COMMAND_OK")


def test_send_ignores_empty_response():
    sender = Mock()

    response_sender = ConnectionSupervisorCommandResponseSender(
        sender
    )

    response_sender.send("")

    sender.assert_not_called()


def test_send_ignores_none_response():
    sender = Mock()

    response_sender = ConnectionSupervisorCommandResponseSender(
        sender
    )

    response_sender.send(None)

    sender.assert_not_called()

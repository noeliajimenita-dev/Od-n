from src.telegram.connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)


def test_connect_command_requires_bot():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.CONNECT,
        bot_name="bot_1",
    )

    assert request.requires_bot() is True


def test_disconnect_command_requires_bot():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.DISCONNECT,
        bot_name="bot_1",
    )

    assert request.requires_bot() is True


def test_recover_command_requires_bot():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.RECOVER,
        bot_name="bot_1",
    )

    assert request.requires_bot() is True


def test_status_command_does_not_require_bot():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.STATUS,
    )

    assert request.requires_bot() is False

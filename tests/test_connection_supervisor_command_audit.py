from src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)


def test_audit_is_created_from_successful_result():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.CONNECT,
        bot_name="bot_1",
    )

    result = ConnectionCommandResult.ok(
        message="Bot conectado correctamente.",
        bot_name="bot_1",
    )

    audit = ConnectionCommandAudit.from_result(request, result)

    assert audit.command == "CONNECT"
    assert audit.bot_name == "bot_1"
    assert audit.success is True
    assert audit.message == "Bot conectado correctamente."
    assert audit.audit_id
    assert audit.timestamp is not None


def test_audit_is_created_from_error_result():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.DISCONNECT,
        bot_name="bot_1",
    )

    result = ConnectionCommandResult.error(
        message="No se pudo desconectar el bot.",
        bot_name="bot_1",
    )

    audit = ConnectionCommandAudit.from_result(request, result)

    assert audit.command == "DISCONNECT"
    assert audit.bot_name == "bot_1"
    assert audit.success is False
    assert audit.message == "No se pudo desconectar el bot."
    assert audit.audit_id
    assert audit.timestamp is not Nonefrom src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)


def test_audit_is_created_from_successful_result():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.CONNECT,
        bot_name="bot_1",
    )

    result = ConnectionCommandResult.ok(
        message="Bot conectado correctamente.",
        bot_name="bot_1",
    )

    audit = ConnectionCommandAudit.from_result(request, result)

    assert audit.command == "CONNECT"
    assert audit.bot_name == "bot_1"
    assert audit.success is True
    assert audit.message == "Bot conectado correctamente."
    assert audit.audit_id
    assert audit.timestamp is not None


def test_audit_is_created_from_error_result():
    request = ConnectionCommandRequest(
        command=ConnectionCommand.DISCONNECT,
        bot_name="bot_1",
    )

    result = ConnectionCommandResult.error(
        message="No se pudo desconectar el bot.",
        bot_name="bot_1",
    )

    audit = ConnectionCommandAudit.from_result(request, result)

    assert audit.command == "DISCONNECT"
    assert audit.bot_name == "bot_1"
    assert audit.success is False
    assert audit.message == "No se pudo desconectar el bot."
    assert audit.audit_id
    assert audit.timestamp is not Nonesrc/telegram/connection_supervisor_command_audit.py

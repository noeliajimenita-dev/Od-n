from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)


def test_success_result():
    result = ConnectionCommandResult.ok(
        message="Bot conectado correctamente.",
        bot_name="bot_1",
    )

    assert result.success is True
    assert result.message == "Bot conectado correctamente."
    assert result.bot_name == "bot_1"


def test_error_result():
    result = ConnectionCommandResult.error(
        message="No se pudo conectar el bot.",
        bot_name="bot_1",
    )

    assert result.success is False
    assert result.message == "No se pudo conectar el bot."
    assert result.bot_name == "bot_1"


def test_result_without_bot():
    result = ConnectionCommandResult.ok(
        message="Estado consultado.",
    )

    assert result.success is True
    assert result.bot_name is None

from src.telegram.command import TelegramCommand
from src.telegram.default_handler import DefaultTelegramHandler
from src.telegram.message import TelegramMessage


def test_handle_message():
    handler = DefaultTelegramHandler()

    message = TelegramMessage.create(
        chat_id="123",
        text="Hola",
        bot_name="supervisor",
    )

    response = handler.handle_message(message)

    assert response.success
    assert response.bot_name == "supervisor"
    assert "Mensaje recibido" in response.text


def test_handle_empty_message():
    handler = DefaultTelegramHandler()

    message = TelegramMessage.create(
        chat_id="123",
        text="   ",
        bot_name="worker_1",
    )

    response = handler.handle_message(message)

    assert not response.success
    assert "vacío" in response.text


def test_handle_command():
    handler = DefaultTelegramHandler()

    command = TelegramCommand.parse("/status")

    assert command is not None

    response = handler.handle_command(command)

    assert response.success
    assert "status" in response.text

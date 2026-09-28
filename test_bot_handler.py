from src.telegram.bot import TelegramBot
from src.telegram.bot_handler import TelegramBotHandler


def test_handle_message():
    bot = TelegramBot(
        name="worker_1",
        token_env_variable="TELEGRAM_WORKER_1_BOT_TOKEN",
    )

    handler = TelegramBotHandler(bot)

    response = handler.handle_message(
        chat_id="123",
        text="Hola Odin",
    )

    assert response.success
    assert response.bot_name == "worker_1"


def test_handle_command():
    bot = TelegramBot(
        name="supervisor",
        token_env_variable="TELEGRAM_SUPERVISOR_BOT_TOKEN",
    )

    handler = TelegramBotHandler(bot)

    response = handler.handle_command("/status")

    assert response.success
    assert "status" in response.text


def test_invalid_command():
    bot = TelegramBot(
        name="worker_2",
        token_env_variable="TELEGRAM_WORKER_2_BOT_TOKEN",
    )

    handler = TelegramBotHandler(bot)

    response = handler.handle_command("hola")

    assert not response.success

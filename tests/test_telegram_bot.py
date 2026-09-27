from src.telegram.bot import TelegramBot


def test_telegram_bot_creation():
    bot = TelegramBot(
        name="supervisor",
        token_env_variable="TELEGRAM_SUPERVISOR_BOT_TOKEN",
    )

    assert bot.name == "supervisor"
    assert bot.token_env_variable == "TELEGRAM_SUPERVISOR_BOT_TOKEN"
    assert bot.enabled is True


def test_telegram_bot_is_configured():
    bot = TelegramBot(
        name="worker_1",
        token_env_variable="TELEGRAM_WORKER_1_BOT_TOKEN",
    )

    assert bot.is_configured() is True


def test_telegram_bot_without_environment_variable():
    bot = TelegramBot(
        name="worker_1",
        token_env_variable="",
    )

    assert bot.is_configured() is False


def test_telegram_bot_can_be_disabled():
    bot = TelegramBot(
        name="worker_2",
        token_env_variable="TELEGRAM_WORKER_2_BOT_TOKEN",
        enabled=False,
    )

    assert bot.enabled is False

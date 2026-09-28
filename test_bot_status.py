from src.telegram.bot_status import TelegramBotStatus


def test_bot_status_ready():
    status = TelegramBotStatus(
        bot_name="worker_1",
        enabled=True,
        token_configured=True,
    )

    assert status.is_ready()
    assert not status.is_connected()


def test_bot_status_disabled():
    status = TelegramBotStatus(
        bot_name="worker_2",
        enabled=False,
        token_configured=True,
    )

    assert not status.is_ready()


def test_bot_status_without_token():
    status = TelegramBotStatus(
        bot_name="worker_3",
        enabled=True,
        token_configured=False,
    )

    assert not status.is_ready()


def test_bot_status_connected():
    status = TelegramBotStatus(
        bot_name="supervisor",
        enabled=True,
        token_configured=True,
        connected=True,
    )

    assert status.is_ready()
    assert status.is_connected()

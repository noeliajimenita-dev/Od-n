from src.telegram.telegram_manager import TelegramManager


def test_telegram_manager_creates_six_clients():
    manager = TelegramManager()

    clients = manager.get_all_clients()

    assert len(clients) == 6


def test_telegram_manager_contains_supervisor():
    manager = TelegramManager()

    client = manager.get_client("supervisor")

    assert client.bot_name == "supervisor"


def test_telegram_manager_contains_all_workers():
    manager = TelegramManager()

    clients = manager.get_all_clients()

    for number in range(1, 6):
        assert f"worker_{number}" in clients


def test_unknown_bot_raises_error():
    manager = TelegramManager()

    try:
        manager.get_client("unknown_bot")
        assert False
    except KeyError:
        assert True

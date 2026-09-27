from src.telegram.registry import create_bot_registry
from src.telegram.status import get_telegram_status


def test_telegram_status_default():
    status = get_telegram_status()

    assert status["total_bots"] == 6
    assert status["enabled_bots"] == 6
    assert status["configured_bots"] == 6


def test_telegram_status_contains_all_bots():
    status = get_telegram_status()

    expected_bots = {
        "supervisor",
        "worker_1",
        "worker_2",
        "worker_3",
        "worker_4",
        "worker_5",
    }

    assert set(status["bots"]) == expected_bots


def test_telegram_status_with_disabled_bot():
    registry = create_bot_registry()

    registry["worker_2"].enabled = False

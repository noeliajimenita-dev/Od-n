from src.telegram.bot_status import TelegramBotStatus
from src.telegram.status_report import create_status_report


def test_create_status_report():
    statuses = [
        TelegramBotStatus(
            bot_name="supervisor",
            enabled=True,
            token_configured=True,
            connected=True,
        ),
        TelegramBotStatus(
            bot_name="worker_1",
            enabled=True,
            token_configured=True,
            connected=True,
        ),
        TelegramBotStatus(
            bot_name="worker_2",
            enabled=True,
            token_configured=False,
        ),
    ]

    report = create_status_report(statuses)

    assert report["total_bots"] == 3
    assert report["ready_bots"] == 2
    assert report["connected_bots"] == 2
    assert report["offline_bots"] == 1


def test_empty_status_report():
    report = create_status_report([])

    assert report["total_bots"] == 0
    assert report["ready_bots"] == 0
    assert report["connected_bots"] == 0
    assert report["offline_bots"] == 0

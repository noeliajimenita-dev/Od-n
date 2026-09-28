from .bot_status import TelegramBotStatus


def create_status_report(
    statuses: list[TelegramBotStatus],
) -> dict:
    total = len(statuses)
    ready = sum(status.is_ready() for status in statuses)
    connected = sum(status.is_connected() for status in statuses)

    return {
        "total_bots": total,
        "ready_bots": ready,
        "connected_bots": connected,
        "offline_bots": total - connected,
    }

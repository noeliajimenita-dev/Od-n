from .connection_service import TelegramConnectionService


def get_connection_service_status(
    service: TelegramConnectionService,
) -> dict:
    statuses = service.get_all_status()

    connected_bots = [
        bot_name
        for bot_name, status in statuses.items()
        if status["connected"]
    ]

    disconnected_bots = [
        bot_name
        for bot_name, status in statuses.items()
        if not status["connected"]
    ]

    return {
        "total_bots": len(statuses),
        "connected_bots": len(connected_bots),
        "disconnected_bots": len(disconnected_bots),
        "connected_bot_names": connected_bots,
        "disconnected_bot_names": disconnected_bots,
    }

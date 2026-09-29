from .connection_supervisor_command_service import (
    TelegramConnectionSupervisorCommandService,
)
from .connection_supervisor_command_service_status import (
    get_connection_command_service_status,
)


def build_connection_command_service_report(
    service: TelegramConnectionSupervisorCommandService,
) -> str:
    status = get_connection_command_service_status(service)

    service_status = "AVAILABLE" if status.available else "UNAVAILABLE"

    return (
        "TELEGRAM COMMAND SERVICE\n"
        f"Status: {service_status}"
    )

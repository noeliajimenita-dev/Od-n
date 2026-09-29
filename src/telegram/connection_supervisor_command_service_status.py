from dataclasses import dataclass

from .connection_supervisor_command_service import (
    TelegramConnectionSupervisorCommandService,
)


@dataclass(frozen=True)
class ConnectionCommandServiceStatus:
    available: bool


def get_connection_command_service_status(
    service: TelegramConnectionSupervisorCommandService,
) -> ConnectionCommandServiceStatus:
    return ConnectionCommandServiceStatus(
        available=service.router is not None
        and service.executor is not None
    )

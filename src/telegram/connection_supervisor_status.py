from dataclasses import dataclass

from .connection_supervisor import TelegramConnectionSupervisor


@dataclass(frozen=True)
class TelegramConnectionSupervisorStatus:
    total_bots: int
    connected_bots: int
    disconnected_bots: int
    all_connected: bool


def get_connection_supervisor_status(
    supervisor: TelegramConnectionSupervisor,
) -> TelegramConnectionSupervisorStatus:
    connected = supervisor.connected_bots()
    disconnected = supervisor.disconnected_bots()

    total = len(connected) + len(disconnected)

    return TelegramConnectionSupervisorStatus(
        total_bots=total,
        connected_bots=len(connected),
        disconnected_bots=len(disconnected),
        all_connected=supervisor.all_connected(),
    )

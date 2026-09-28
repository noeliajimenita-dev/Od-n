from .connection_manager import TelegramConnectionManager
from .connection_state import TelegramConnectionState


def get_connection_status(
    manager: TelegramConnectionManager,
) -> dict:
    states = manager.get_all_states()

    counts = {
        state.value: 0
        for state in TelegramConnectionState
    }

    for state in states.values():
        counts[state.value] += 1

    return {
        "total_bots": len(states),
        "states": counts,
        "connected_bots": counts[TelegramConnectionState.CONNECTED.value],
        "error_bots": counts[TelegramConnectionState.ERROR.value],
        "stopped_bots": counts[TelegramConnectionState.STOPPED.value],
    }

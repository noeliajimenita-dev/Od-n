"""
Connection Supervisor module for Telegram bot connection management.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import datetime


@dataclass
class ConnectionSupervisorState:
    """Represents the operational state of the connection supervisor."""
    active: bool = True
    active_connections: int = 0
    total_commands_processed: int = 0
    last_action_timestamp: Optional[datetime.datetime] = None


class ConnectionSupervisor:
    """Supervises Telegram bot connections and handles lifecycle commands."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.state = ConnectionSupervisorState()
        self._bot_statuses: Dict[str, bool] = {}

    def is_active(self) -> bool:
        """Returns whether the supervisor is currently active."""
        return self.state.active

    def enable(self) -> None:
        """Enables the supervisor."""
        self.state.active = True

    def disable(self) -> None:
        """Disables the supervisor."""
        self.state.active = False

    def get_bot_status(self, bot_name: str) -> bool:
        """Returns the connection status of a specific bot."""
        return self._bot_statuses.get(bot_name, False)

    def connect_bot(self, bot_name: str) -> bool:
        """Connects a bot if the supervisor is active."""
        if not self.state.active:
            return False

        if not self._bot_statuses.get(bot_name, False):
            self._bot_statuses[bot_name] = True
            self.state.active_connections += 1

        self.state.total_commands_processed += 1
        self.state.last_action_timestamp = datetime.datetime.now(datetime.timezone.utc)
        return True

    def disconnect_bot(self, bot_name: str) -> bool:
        """Disconnects a bot if the supervisor is active."""
        if not self.state.active:
            return False

        if self._bot_statuses.get(bot_name, False):
            self._bot_statuses[bot_name] = False
            self.state.active_connections = max(0, self.state.active_connections - 1)

        self.state.total_commands_processed += 1
        self.state.last_action_timestamp = datetime.datetime.now(datetime.timezone.utc)
        return True

    def get_summary(self) -> Dict[str, Any]:
        """Returns a summary report of the supervisor status."""
        return {
            "active": self.state.active,
            "active_connections": self.state.active_connections,
            "total_commands_processed": self.state.total_commands_processed,
            "connected_bots": [bot for bot, status in self._bot_statuses.items() if status],
        }

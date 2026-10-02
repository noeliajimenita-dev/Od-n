from abc import ABC, abstractmethod
from typing import Any

from .external_account_connection import ExternalAccountConnection
from .external_account_operation import ExternalAccountOperation


class ExternalPlatformConnector(ABC):
    """Base interface for external platform connectors."""

    def __init__(self, service_name: str) -> None:
        if not service_name.strip():
            raise ValueError("service_name cannot be empty")

        self.service_name = service_name

    @abstractmethod
    def connect(
        self,
        account: ExternalAccountConnection,
    ) -> bool:
        """Establish a connection with the external platform."""
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> Any:
        """Execute an operation on the external platform."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(
        self,
        account: ExternalAccountConnection,
    ) -> None:
        """Close the external platform connection."""
        raise NotImplementedError

    def supports(self, action: str) -> bool:
        """Return whether this connector supports an action."""
        return bool(action.strip())

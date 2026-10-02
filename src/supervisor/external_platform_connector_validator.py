from .external_platform_connector import ExternalPlatformConnector


class ExternalPlatformConnectorValidator:
    """Validates external platform connectors."""

    def validate(
        self,
        connector: ExternalPlatformConnector,
    ) -> bool:
        if not connector.service_name.strip():
            raise ValueError("service_name cannot be empty")

        if not hasattr(connector, "connect"):
            raise ValueError("Connector must implement connect")

        if not hasattr(connector, "execute"):
            raise ValueError("Connector must implement execute")

        if not hasattr(connector, "disconnect"):
            raise ValueError("Connector must implement disconnect")

        return True

    def validate_action(
        self,
        connector: ExternalPlatformConnector,
        action: str,
    ) -> bool:
        self.validate(connector)

        if not action.strip():
            raise ValueError("action cannot be empty")

        if not connector.supports(action):
            raise ValueError(
                f"Unsupported action '{action}' "
                f"for service '{connector.service_name}'"
            )

        return True

    def is_valid(
        self,
        connector: ExternalPlatformConnector,
    ) -> bool:
        try:
            self.validate(connector)
            return True
        except ValueError:
            return False

    def supports_action(
        self,
        connector: ExternalPlatformConnector,
        action: str,
    ) -> bool:
        try:
            return self.validate_action(connector, action)
        except ValueError:
            return False

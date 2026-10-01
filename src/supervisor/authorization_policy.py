class AuthorizationPolicy:
    """Defines which Supervisor actions require user authorization."""

    SENSITIVE_ACTIONS = {
        "spend_money",
        "purchase_service",
        "change_credentials",
        "change_sensitive_permissions",
        "publish_application",
        "external_action",
        "deliver_client_work",
        "connect_account",
    }

    def requires_authorization(self, action: str) -> bool:
        if not action or not action.strip():
            return False

        normalized_action = action.strip().lower()
        return normalized_action in self.SENSITIVE_ACTIONS

    def validate_action(self, action: str) -> None:
        if not action or not action.strip():
            raise ValueError("Action cannot be empty")

    def is_sensitive(self, action: str) -> bool:
        return self.requires_authorization(action)

    def get_sensitive_actions(self) -> list[str]:
        return sorted(self.SENSITIVE_ACTIONS)

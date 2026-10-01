from .account_connection_session_service import (
    AccountConnectionSessionService,
)
from .credential_vault import CredentialVault


class AccountConnectionSecurity:
    """Validates security requirements before account connection."""

    def __init__(
        self,
        session_service: AccountConnectionSessionService | None = None,
        credential_vault: CredentialVault | None = None,
    ) -> None:
        self.session_service = (
            session_service or AccountConnectionSessionService()
        )
        self.credential_vault = credential_vault or CredentialVault()

    def validate_session(self, session_id: str) -> bool:
        session = self.session_service.get(session_id)

        if session is None:
            return False

        if session.is_cancelled or session.is_completed:
            return False

        return True

    def validate_credentials(self, credential_ref: str) -> bool:
        if not credential_ref or not credential_ref.strip():
            return False

        return self.credential_vault.exists(credential_ref)

    def authorize_connection(
        self,
        session_id: str,
        credential_ref: str,
    ) -> bool:
        if not self.validate_session(session_id):
            return False

        if not self.validate_credentials(credential_ref):
            return False

        return True

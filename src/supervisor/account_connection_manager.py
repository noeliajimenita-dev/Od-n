from .connected_account import ConnectedAccount
from .connected_account_service import ConnectedAccountService
from .credential_vault import CredentialVault


class AccountConnectionManager:
    """Coordinates secure external account connections."""

    def __init__(
        self,
        account_service: ConnectedAccountService | None = None,
        credential_vault: CredentialVault | None = None,
    ) -> None:
        self.account_service = (
            account_service or ConnectedAccountService()
        )
        self.credential_vault = credential_vault or CredentialVault()

    def connect_account(
        self,
        account_id: str,
        service: str,
        username: str,
        password: str,
    ) -> ConnectedAccount:
        credential_ref = f"credential_{account_id}"

        self.credential_vault.store(
            credential_ref=credential_ref,
            username=username,
            password=password,
        )

        try:
            return self.account_service.connect(
                account_id=account_id,
                service=service,
                username=username,
                credential_ref=credential_ref,
            )
        except Exception:
            self.credential_vault.delete(credential_ref)
            raise

    def disconnect_account(
        self,
        account_id: str,
        delete_credentials: bool = True,
    ) -> ConnectedAccount:
        account = self.account_service.disconnect(account_id)

        if delete_credentials:
            self.credential_vault.delete(account.credential_ref)

        return account

    def get_account(self, account_id: str) -> ConnectedAccount | None:
        return self.account_service.get(account_id)

    def has_credentials(self, account_id: str) -> bool:
        account = self.get_account(account_id)

        if account is None:
            return False

        return self.credential_vault.exists(account.credential_ref)

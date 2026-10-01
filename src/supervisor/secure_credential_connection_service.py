from .secure_credential_submission import SecureCredentialSubmission
from .secure_credential_submission_service import (
    SecureCredentialSubmissionService,
)
from .secure_credential_vault_adapter import (
    SecureCredentialVaultAdapter,
)


class SecureCredentialConnectionService:
    """Connects secure credential submissions with the credential vault."""

    def __init__(
        self,
        submission_service: SecureCredentialSubmissionService | None = None,
        vault_adapter: SecureCredentialVaultAdapter | None = None,
    ) -> None:
        self.submission_service = (
            submission_service
            or SecureCredentialSubmissionService()
        )
        self.vault_adapter = (
            vault_adapter
            or SecureCredentialVaultAdapter()
        )

    def register_submission(
        self,
        submission: SecureCredentialSubmission,
    ) -> SecureCredentialSubmission:
        saved = self.submission_service.submit(submission)

        if not self.vault_adapter.exists(saved.credential_ref):
            raise ValueError(
                f"Credential reference not found in vault: "
                f"{saved.credential_ref}"
            )

        return saved

    def is_ready(
        self,
        request_id: str,
    ) -> bool:
        submission = self.submission_service.get(request_id)

        if submission is None:
            return False

        return self.vault_adapter.exists(
            submission.credential_ref
        )

    def get_credential_reference(
        self,
        request_id: str,
    ) -> str | None:
        submission = self.submission_service.get(request_id)

        if submission is None:
            return None

        return submission.credential_ref

    def remove_submission(
        self,
        request_id: str,
        delete_credential: bool = False,
    ) -> bool:
        submission = self.submission_service.get(request_id)

        if submission is None:
            return False

        if delete_credential:
            self.vault_adapter.delete(
                submission.credential_ref
            )

        return self.submission_service.delete(request_id)

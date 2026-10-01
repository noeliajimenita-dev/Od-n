from .secure_credential_submission import SecureCredentialSubmission
from .secure_credential_submission_repository import (
    SecureCredentialSubmissionRepository,
)
from .secure_credential_submission_validator import (
    SecureCredentialSubmissionValidator,
)


class SecureCredentialSubmissionService:
    """Service layer for secure credential submissions."""

    def __init__(
        self,
        repository: SecureCredentialSubmissionRepository | None = None,
        validator: SecureCredentialSubmissionValidator | None = None,
    ) -> None:
        self.repository = (
            repository or SecureCredentialSubmissionRepository()
        )
        self.validator = (
            validator or SecureCredentialSubmissionValidator()
        )

    def submit(
        self,
        submission: SecureCredentialSubmission,
    ) -> SecureCredentialSubmission:
        self.validator.validate(submission)
        self.validator.validate_reference(submission)

        return self.repository.save(submission)

    def get(
        self,
        request_id: str,
    ) -> SecureCredentialSubmission | None:
        return self.repository.get(request_id)

    def exists(self, request_id: str) -> bool:
        return self.repository.exists(request_id)

    def get_by_session(
        self,
        session_id: str,
    ) -> list[SecureCredentialSubmission]:
        return self.repository.list_by_session(session_id)

    def delete(self, request_id: str) -> bool:
        return self.repository.delete(request_id)

    def count(self) -> int:
        return self.repository.count()

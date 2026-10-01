from .secure_credential_submission import SecureCredentialSubmission


class SecureCredentialSubmissionRepository:
    """Repository for secure credential submissions."""

    def __init__(self) -> None:
        self._submissions: dict[str, SecureCredentialSubmission] = {}

    def save(
        self,
        submission: SecureCredentialSubmission,
    ) -> SecureCredentialSubmission:
        self._submissions[submission.request_id] = submission
        return submission

    def get(
        self,
        request_id: str,
    ) -> SecureCredentialSubmission | None:
        return self._submissions.get(request_id)

    def exists(self, request_id: str) -> bool:
        return request_id in self._submissions

    def update(
        self,
        submission: SecureCredentialSubmission,
    ) -> SecureCredentialSubmission:
        if submission.request_id not in self._submissions:
            raise ValueError(
                f"Submission not found: {submission.request_id}"
            )

        self._submissions[submission.request_id] = submission
        return submission

    def delete(self, request_id: str) -> bool:
        if request_id not in self._submissions:
            return False

        del self._submissions[request_id]
        return True

    def list_all(self) -> list[SecureCredentialSubmission]:
        return list(self._submissions.values())

    def list_by_session(
        self,
        session_id: str,
    ) -> list[SecureCredentialSubmission]:
        return [
            submission
            for submission in self._submissions.values()
            if submission.session_id == session_id
        ]

    def count(self) -> int:
        return len(self._submissions)

    def clear(self) -> None:
        self._submissions.clear()

from .secure_credential_submission import SecureCredentialSubmission


class SecureCredentialSubmissionValidator:
    """Validates secure credential submissions."""

    def validate(
        self,
        submission: SecureCredentialSubmission,
    ) -> bool:
        if not isinstance(
            submission,
            SecureCredentialSubmission,
        ):
            raise TypeError(
                "submission must be a SecureCredentialSubmission"
            )

        if not submission.request_id.strip():
            raise ValueError("request_id cannot be empty")

        if not submission.session_id.strip():
            raise ValueError("session_id cannot be empty")

        if not submission.credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")

        if submission.status != "submitted":
            raise ValueError(
                f"Invalid submission status: {submission.status}"
            )

        return True

    def validate_reference(
        self,
        submission: SecureCredentialSubmission,
    ) -> bool:
        self.validate(submission)

        if not submission.credential_ref.startswith("credential_"):
            raise ValueError(
                "Invalid credential reference format"
            )

        return True

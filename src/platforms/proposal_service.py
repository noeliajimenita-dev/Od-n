from __future__ import annotations

from .job_service import JobService
from .platform_account_service import PlatformAccountService
from .proposal import Proposal
from .proposal_repository import ProposalRepository


class ProposalService:
    """Gestiona propuestas y controla su autorización."""

    def __init__(
        self,
        repository: ProposalRepository,
        job_service: JobService,
        account_service: PlatformAccountService,
    ) -> None:
        if repository is None:
            raise ValueError("repository cannot be None")

        if job_service is None:
            raise ValueError("job_service cannot be None")

        if account_service is None:
            raise ValueError(
                "account_service cannot be None"
            )

        self.repository = repository
        self.job_service = job_service
        self.account_service = account_service

    def create(
        self,
        proposal: Proposal,
    ) -> Proposal:
        if proposal is None:
            raise ValueError(
                "proposal cannot be None"
            )

        if self.repository.exists(
            proposal.proposal_id
        ):
            raise ValueError(
                "Proposal already exists: "
                f"{proposal.proposal_id}"
            )

        job = self.job_service.get(proposal.job_id)

        if job is None:
            raise ValueError(
                f"Job not found: {proposal.job_id}"
            )

        if not job.is_eligible():
            raise ValueError(
                "Proposal can only be created "
                "for an eligible job"
            )

        account = self.account_service.get(
            proposal.account_id
        )

        if account is None:
            raise ValueError(
                "Account not found: "
                f"{proposal.account_id}"
            )

        if not account.is_ready():
            raise ValueError(
                "Account is not ready"
            )

        return self.repository.save(proposal)

    def get(
        self,
        proposal_id: str,
    ) -> Proposal | None:
        return self.repository.get(proposal_id)

    def mark_ready(
        self,
        proposal_id: str,
    ) -> Proposal:
        proposal = self._require(proposal_id)

        proposal.mark_ready()

        return self.repository.save(proposal)

    def authorize(
        self,
        proposal_id: str,
        authorization_id: str,
    ) -> Proposal:
        proposal = self._require(proposal_id)

        proposal.mark_authorized(
            authorization_id
        )

        return self.repository.save(proposal)

    def submit(
        self,
        proposal_id: str,
    ) -> Proposal:
        proposal = self._require(proposal_id)

        if proposal.requires_authorization():
            raise PermissionError(
                "Proposal requires authorization"
            )

        if not proposal.is_authorized():
            raise PermissionError(
                "Proposal is not authorized"
            )

        proposal.mark_submitted()

        return self.repository.save(proposal)

    def reject(
        self,
        proposal_id: str,
    ) -> Proposal:
        proposal = self._require(proposal_id)

        proposal.mark_rejected()

        return self.repository.save(proposal)

    def list_pending_authorization(
        self,
    ) -> list[Proposal]:
        return self.repository.list_pending_authorization()

    def list_ready(self) -> list[Proposal]:
        return self.repository.list_by_status("ready")

    def list_submitted(self) -> list[Proposal]:
        return self.repository.list_submitted()

    def list_by_job(
        self,
        job_id: str,
    ) -> list[Proposal]:
        return self.repository.list_by_job(job_id)

    def count(self) -> int:
        return self.repository.count()

    def _require(
        self,
        proposal_id: str,
    ) -> Proposal:
        proposal = self.get(proposal_id)

        if proposal is None:
            raise ValueError(
                f"Proposal not found: {proposal_id}"
            )

        return proposal

    def __repr__(self) -> str:
        return (
            "ProposalService("
            f"proposals={self.count()}, "
            f"pending="
            f"{len(self.list_pending_authorization())}"
            ")"
                  )

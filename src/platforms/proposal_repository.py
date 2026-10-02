from __future__ import annotations

from .proposal import Proposal


class ProposalRepository:
    """Repositorio en memoria de propuestas."""

    def __init__(self) -> None:
        self._proposals: dict[str, Proposal] = {}

    def save(self, proposal: Proposal) -> Proposal:
        if proposal is None:
            raise ValueError("proposal cannot be None")

        self._proposals[proposal.proposal_id] = proposal
        return proposal

    def get(self, proposal_id: str) -> Proposal | None:
        if not proposal_id or not proposal_id.strip():
            return None

        return self._proposals.get(proposal_id)

    def exists(self, proposal_id: str) -> bool:
        return self.get(proposal_id) is not None

    def delete(self, proposal_id: str) -> bool:
        if proposal_id not in self._proposals:
            return False

        del self._proposals[proposal_id]
        return True

    def list_all(self) -> list[Proposal]:
        return list(self._proposals.values())

    def list_by_job(self, job_id: str) -> list[Proposal]:
        job_id = job_id.strip()

        return [
            proposal
            for proposal in self._proposals.values()
            if proposal.job_id == job_id
        ]

    def list_by_account(
        self,
        account_id: str,
    ) -> list[Proposal]:
        account_id = account_id.strip()

        return [
            proposal
            for proposal in self._proposals.values()
            if proposal.account_id == account_id
        ]

    def list_by_status(
        self,
        status: str,
    ) -> list[Proposal]:
        status = status.strip().lower()

        return [
            proposal
            for proposal in self._proposals.values()
            if proposal.status.lower() == status
        ]

    def list_pending_authorization(
        self,
    ) -> list[Proposal]:
        return [
            proposal
            for proposal in self._proposals.values()
            if proposal.authorization_required
        ]

    def list_submitted(self) -> list[Proposal]:
        return self.list_by_status("submitted")

    def count(self) -> int:
        return len(self._proposals)

    def count_by_status(self, status: str) -> int:
        return len(self.list_by_status(status))

    def clear(self) -> None:
        self._proposals.clear()

    def __repr__(self) -> str:
        return (
            "ProposalRepository("
            f"proposals={self.count()}"
            ")"
      )

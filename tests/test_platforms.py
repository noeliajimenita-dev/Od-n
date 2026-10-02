from __future__ import annotations

import pytest

from src.platforms.job import Job
from src.platforms.job_repository import JobRepository
from src.platforms.job_service import JobService
from src.platforms.platform_account import PlatformAccount
from src.platforms.platform_account_repository import (
    PlatformAccountRepository,
)
from src.platforms.platform_account_service import (
    PlatformAccountService,
)
from src.platforms.proposal import Proposal
from src.platforms.proposal_repository import (
    ProposalRepository,
)
from src.platforms.proposal_service import ProposalService


def build_system():
    account_repository = PlatformAccountRepository()
    account_service = PlatformAccountService(
        account_repository
    )

    job_repository = JobRepository()
    job_service = JobService(job_repository)

    proposal_repository = ProposalRepository()
    proposal_service = ProposalService(
        repository=proposal_repository,
        job_service=job_service,
        account_service=account_service,
    )

    return (
        account_service,
        job_service,
        proposal_service,
    )


def create_ready_account(
    account_service: PlatformAccountService,
) -> PlatformAccount:
    account = PlatformAccount(
        account_id="account_1",
        platform="upwork",
        username="odin_user",
        credential_ref="credential_account_1",
    )

    account_service.register(account)
    account_service.verify("account_1")

    return account_service.get("account_1")


def create_eligible_job(
    job_service: JobService,
) -> Job:
    job = Job(
        job_id="job_1",
        platform="upwork",
        title="Python automation",
        description="Build an automation system",
        url="https://example.com/job/1",
        price=500.0,
        currency="USD",
    )

    job.add_skill("python")
    job_service.add(job)

    assert job_service.evaluate(
        job_id="job_1",
        required_skills={"python"},
        minimum_price=300.0,
    )

    return job_service.get("job_1")


def test_account_becomes_ready_after_verification():
    (
        account_service,
        _,
        _,
    ) = build_system()

    account = create_ready_account(
        account_service
    )

    assert account is not None
    assert account.is_connected()
    assert account.is_ready()


def test_job_can_be_added_and_evaluated():
    (
        _,
        job_service,
        _,
    ) = build_system()

    job = create_eligible_job(
        job_service
    )

    assert job is not None
    assert job.is_eligible()
    assert job.status == "eligible"


def test_job_below_minimum_price_is_discarded():
    (
        _,
        job_service,
        _,
    ) = build_system()

    job = Job(
        job_id="job_low",
        platform="upwork",
        title="Small task",
        description="Low value task",
        price=50.0,
    )

    job_service.add(job)

    accepted = job_service.evaluate(
        job_id="job_low",
        minimum_price=100.0,
    )

    assert accepted is False
    assert job.status == "discarded"


def test_proposal_requires_ready_account():
    (
        account_service,
        job_service,
        proposal_service,
    ) = build_system()

    account = PlatformAccount(
        account_id="account_unverified",
        platform="upwork",
        username="user",
        credential_ref="credential_account_unverified",
    )

    account_service.register(account)

    create_eligible_job(job_service)

    proposal = Proposal(
        proposal_id="proposal_1",
        job_id="job_1",
        account_id="account_unverified",
        message="I can complete this project.",
        price=500.0,
        delivery_hours=20.0,
    )

    with pytest.raises(ValueError):
        proposal_service.create(proposal)


def test_proposal_can_be_created_with_ready_account():
    (
        account_service,
        job_service,
        proposal_service,
    ) = build_system()

    create_ready_account(account_service)
    create_eligible_job(job_service)

    proposal = Proposal(
        proposal_id="proposal_2",
        job_id="job_1",
        account_id="account_1",
        message="I can complete this project.",
        price=500.0,
        delivery_hours=20.0,
    )

    created = proposal_service.create(
        proposal
    )

    assert created is proposal
    assert created.status == "draft"


def test_proposal_can_be_marked_ready():
    (
        account_service,
        job_service,
        proposal_service,
    ) = build_system()

    create_ready_account(account_service)
    create_eligible_job(job_service)

    proposal_service.create(
        Proposal(
            proposal_id="proposal_3",
            job_id="job_1",
            account_id="account_1",
            message="Ready proposal.",
            price=500.0,
            delivery_hours=20.0,
        )
    )

    proposal = proposal_service.mark_ready(
        "proposal_3"
    )

    assert proposal.is_ready()


def test_submission_is_blocked_without_authorization():
    (
        account_service,
        job_service,
        proposal_service,
    ) = build_system()

    create_ready_account(account_service)
    create_eligible_job(job_service)

    proposal_service.create(
        Proposal(
            proposal_id="proposal_4",
            job_id="job_1",
            account_id="account_1",
            message="Authorization test.",
            price=500.0,
            delivery_hours=20.0,
        )
    )

    proposal_service.mark_ready(
        "proposal_4"
    )

    with pytest.raises(PermissionError):
        proposal_service.submit(
            "proposal_4"
        )


def test_authorized_proposal_can_be_submitted():
    (
        account_service,
        job_service,
        proposal_service,
    ) = build_system()

    create_ready_account(account_service)
    create_eligible_job(job_service)

    proposal_service.create(
        Proposal(
            proposal_id="proposal_5",
            job_id="job_1",
            account_id="account_1",
            message="Authorized proposal.",
            price=500.0,
            delivery_hours=20.0,
        )
    )

    proposal_service.mark_ready(
        "proposal_5"
    )

    proposal_service.authorize(
        proposal_id="proposal_5",
        authorization_id="auth_1",
    )

    submitted = proposal_service.submit(
        "proposal_5"
    )

    assert submitted.is_submitted()
    assert submitted.authorization_id == "auth_1"


def test_pending_authorization_is_reported():
    (
        account_service,
        job_service,
        proposal_service,
    ) = build_system()

    create_ready_account(account_service)
    create_eligible_job(job_service)

    proposal_service.create(
        Proposal(
            proposal_id="proposal_6",
            job_id="job_1",
            account_id="account_1",
            message="Pending authorization.",
            price=500.0,
            delivery_hours=20.0,
        )
    )

    pending = (
        proposal_service.list_pending_authorization()
    )

    assert len(pending) == 1
    assert pending[0].proposal_id == "proposal_6"


def test_proposal_rejection_changes_status():
    (
        account_service,
        job_service,
        proposal_service,
    ) = build_system()

    create_ready_account(account_service)
    create_eligible_job(job_service)

    proposal_service.create(
        Proposal(
            proposal_id="proposal_7",
            job_id="job_1",
            account_id="account_1",
            message="Reject test.",
            price=500.0,
            delivery_hours=20.0,
        )
    )

    rejected = proposal_service.reject(
        "proposal_7"
    )

    assert rejected.status == "rejected"


def test_job_and_proposal_are_link

from src.permissions.actions import (
    PermissionAction,
    PermissionLevel,
)
from src.permissions.checker import check_permission


def test_allowed_action():
    decision = check_permission(
        "worker_1",
        PermissionAction.READ_CODE,
    )

    assert decision.level == PermissionLevel.ALLOWED
    assert decision.allowed is True
    assert decision.requires_approval is False


def test_sensitive_action_requires_approval():
    decision = check_permission(
        "worker_1",
        PermissionAction.MERGE_MAIN,
    )

    assert decision.level == PermissionLevel.REQUIRES_APPROVAL
    assert decision.allowed is False
    assert decision.requires_approval is True


def test_money_action_requires_approval():
    decision = check_permission(
        "worker_1",
        PermissionAction.SPEND_MONEY,
    )

    assert decision.level == PermissionLevel.REQUIRES_APPROVAL
    assert decision.allowed is False
    assert decision.requires_approval is True


def test_unknown_role_is_denied():
    decision = check_permission(
        "unknown_role",
        PermissionAction.READ_CODE,
    )

    assert decision.level == PermissionLevel.DENIED
    assert decision.allowed is False
    assert decision.requires_approval is False


def test_decision_contains_role_and_action():
    decision = check_permission(
        "supervisor",
        PermissionAction.RUN_TESTS,
    )

    assert decision.role == "supervisor"
    assert decision.action == PermissionAction.RUN_TESTS

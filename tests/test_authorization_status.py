from src.authorization.manager import AuthorizationManager
from src.authorization.status import get_authorization_status


def test_empty_authorization_status():
    manager = AuthorizationManager()

    status = get_authorization_status(manager)

    assert status["total_requests"] == 0
    assert status["pending"] == 0
    assert status["approved"] == 0
    assert status["denied"] == 0


def test_pending_authorization_status():
    manager = AuthorizationManager()

    manager.create_request(
        action="MERGE_MAIN",
        requester="worker_1",
        reason="Solicitar autorización.",
    )

    status = get_authorization_status(manager)

    assert status["total_requests"] == 1
    assert status["pending"] == 1
    assert status["approved"] == 0
    assert status["denied"] == 0


def test_approved_authorization_status():
    manager = AuthorizationManager()

    request = manager.create_request(
        action="PUBLISH",
        requester="worker_1",
        reason="Solicitar publicación.",
    )

    manager.approve(request.request_id)

    status = get_authorization_status(manager)

    assert status["total_requests"] == 1
    assert status["pending"] == 0
    assert status["approved"] == 1
    assert status["denied"] == 0


def test_denied_authorization_status():
    manager = AuthorizationManager()

    request = manager.create_request(
        action="SPEND_MONEY",
        requester="worker_1",
        reason="Solicitar autorización de gasto.",
    )

    manager.deny(request.request_id)

    status = get_authorization_status(manager)

    assert status["total_requests"] == 1
    assert status["pending"] == 0
    assert status["approved"] == 0
    assert status["denied"] == 1


def test_mixed_authorization_status():
    manager = AuthorizationManager()

    pending = manager.create_request(
        action="MERGE_MAIN",
        requester="worker_1",
        reason="Solicitud pendiente.",
    )

    approved = manager.create_request(
        action="PUBLISH",
        requester="worker_2",
        reason="Solicitud aprobada.",
    )

    denied = manager.create_request(
        action="SPEND_MONEY",
        requester="worker_3",
        reason="Solicitud rechazada.",
    )

    manager.approve(approved.request_id)
    manager.deny(denied.request_id)

    status = get_authorization_status(manager)

    assert pending.is_pending() is True
    assert status["total_requests"] == 3
    assert status["pending"] == 1
    assert status["approved"] == 1
    assert status["denied"] == 1

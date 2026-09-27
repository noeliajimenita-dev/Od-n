from src.authorization.manager import AuthorizationManager


def test_create_request():
    manager = AuthorizationManager()

    request = manager.create_request(
        action="MERGE_MAIN",
        requester="worker_1",
        reason="Cambios preparados y pruebas completadas.",
    )

    assert request.request_id
    assert request.action == "MERGE_MAIN"
    assert request.requester == "worker_1"
    assert manager.count() == 1


def test_get_request():
    manager = AuthorizationManager()

    request = manager.create_request(
        action="PUBLISH",
        requester="worker_2",
        reason="Solicitar publicación.",
    )

    result = manager.get_request(request.request_id)

    assert result is request


def test_get_unknown_request():
    manager = AuthorizationManager()

    result = manager.get_request("unknown-id")

    assert result is None


def test_pending_requests():
    manager = AuthorizationManager()

    manager.create_request(
        action="MERGE_MAIN",
        requester="worker_1",
        reason="Solicitud de merge.",
    )

    manager.create_request(
        action="DEPLOY_PRODUCTION",
        requester="worker_2",
        reason="Solicitud de despliegue.",
    )

    assert manager.count_pending() == 2


def test_approve_request():
    manager = AuthorizationManager()

    request = manager.create_request(
        action="MERGE_MAIN",
        requester="worker_1",
        reason="Cambios listos.",
    )

    result = manager.approve(request.request_id)

    assert result is True
    assert request.approved is True
    assert request.resolved is True
    assert manager.count_pending() == 0


def test_deny_request():
    manager = AuthorizationManager()

    request = manager.create_request(
        action="PUBLISH",
        requester="worker_1",
        reason="Solicitar publicación.",
    )

    result = manager.deny(request.request_id)

    assert result is True
    assert request.approved is False
    assert request.resolved is True
    assert manager.count_pending() == 0


def test_cannot_approve_unknown_request():
    manager = AuthorizationManager()

    result = manager.approve("unknown-id")

    assert result is False


def test_cannot_deny_unknown_request():
    manager = AuthorizationManager()

    result = manager.deny("unknown-id")

    assert result is False


def test_cannot_approve_already_resolved_request():
    manager = AuthorizationManager()

    request = manager.create_request(
        action="SPEND_MONEY",
        requester="supervisor",
        reason="Solicitar autorización de gasto.",
    )

    manager.approve(request.request_id)

    result = manager.approve(request.request_id)

    assert result is False

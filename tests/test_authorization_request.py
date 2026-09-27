from src.authorization.request import AuthorizationRequest


def test_authorization_request_starts_pending():
    request = AuthorizationRequest(
        action="MERGE_MAIN",
        requester="worker_1",
        reason="Cambios listos y pruebas completadas.",
    )

    assert request.approved is False
    assert request.resolved is False
    assert request.is_pending() is True


def test_authorization_request_has_id():
    request = AuthorizationRequest(
        action="SPEND_MONEY",
        requester="supervisor",
        reason="Se necesita contratar un servicio.",
    )

    assert request.request_id
    assert isinstance(request.request_id, str)


def test_authorization_request_can_be_approved():
    request = AuthorizationRequest(
        action="PUBLISH",
        requester="worker_1",
        reason="Publicar la versión aprobada.",
    )

    request.approve()

    assert request.approved is True
    assert request.resolved is True
    assert request.is_pending() is False


def test_authorization_request_can_be_denied():
    request = AuthorizationRequest(
        action="DEPLOY_PRODUCTION",
        requester="worker_1",
        reason="Solicitar despliegue de la versión preparada.",
    )

    request.deny()

    assert request.approved is False
    assert request.resolved is True
    assert request.is_pending() is False


def test_authorization_request_can_include_task_id():
    request = AuthorizationRequest(
        action="MERGE_MAIN",
        requester="worker_2",
        reason="Finalizar tarea.",
        task_id="task-001",
    )

    assert request.task_id == "task-001"

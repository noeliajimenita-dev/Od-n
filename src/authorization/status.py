from .manager import AuthorizationManager


def get_authorization_status(
    manager: AuthorizationManager,
) -> dict:
    """Devuelve un resumen del estado de las autorizaciones."""

    requests = manager.get_all()

    approved = sum(
        1 for request in requests
        if request.resolved and request.approved
    )

    denied = sum(
        1 for request in requests
        if request.resolved and not request.approved
    )

    pending = sum(
        1 for request in requests
        if request.is_pending()
    )

    return {
        "total_requests": len(requests),
        "pending": pending,
        "approved": approved,
        "denied": denied,
    }

from src.telegram.connection_supervisor_command_router import (
    TelegramConnectionSupervisorCommandRouter,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)


class FakeHandler:
    def __init__(self):
        self.received_request = None

    def handle(self, request):
        self.received_request = request
        return "handled"


def test_router_sends_request_to_handler():
    handler = FakeHandler()
    router = TelegramConnectionSupervisorCommandRouter(handler)

    request = ConnectionCommandRequest(
        command=ConnectionCommand.STATUS,
    )

    result = router.route(request)

    assert result == "handled"
    assert handler.received_request is request

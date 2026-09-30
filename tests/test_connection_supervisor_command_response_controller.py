from unittest.mock import Mock

from src.telegram.connection_supervisor_command_response_controller import (
    ConnectionSupervisorCommandResponseController,
)
from src.telegram.connection_supervisor_command_response_integration import (
    ConnectionSupervisorCommandResponseIntegration,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_handle_delegates_request_to_integration():
    integration = Mock(
        spec=ConnectionSupervisorCommandResponseIntegration
    )
    request = Mock(spec=ConnectionCommandRequest)

    integration.execute.return_value = "COMMAND_OK"

    controller = ConnectionSupervisorCommandResponseController(
        integration
    )

    output = controller.handle(request)

    integration.execute.assert_called_once_with(request)
    assert output == "COMMAND_OK"


def test_handle_returns_blocked_response():
    integration = Mock(
        spec=ConnectionSupervisorCommandResponseIntegration
    )
    request = Mock(spec=ConnectionCommandRequest)

    integration.execute.return_value = "COMMAND_BLOCKED"

    controller = ConnectionSupervisorCommandResponseController(
        integration
    )

    output = controller.handle(request)

    integration.execute.assert_called_once_with(request)
    assert output == "COMMAND_BLOCKED"

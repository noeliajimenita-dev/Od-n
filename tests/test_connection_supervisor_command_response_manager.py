from unittest.mock import Mock

from src.telegram.connection_supervisor_command_response_manager import (
    ConnectionSupervisorCommandResponseManager,
)
from src.telegram.connection_supervisor_command_response_service import (
    ConnectionSupervisorCommandResponseService,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)


def test_process_delegates_to_response_service():
    response_service = Mock(
        spec=ConnectionSupervisorCommandResponseService
    )
    result = Mock(spec=ConnectionCommandResult)

    response_service.handle.return_value = "COMMAND_OK"

    manager = ConnectionSupervisorCommandResponseManager(
        response_service
    )

    output = manager.process(result)

    response_service.handle.assert_called_once_with(result)
    assert output == "COMMAND_OK"


def test_process_handles_blocked_command():
    response_service = Mock(
        spec=ConnectionSupervisorCommandResponseService
    )

    response_service.handle.return_value = "COMMAND_BLOCKED"

    manager = ConnectionSupervisorCommandResponseManager(
        response_service
    )

    output = manager.process(None)

    response_service.handle.assert_called_once_with(None)
    assert output == "COMMAND_BLOCKED"

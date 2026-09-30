from unittest.mock import Mock

from src.telegram.connection_supervisor_command_execution import (
    ConnectionSupervisorCommandExecution,
)
from src.telegram.connection_supervisor_command_response_integration import (
    ConnectionSupervisorCommandResponseIntegration,
)
from src.telegram.connection_supervisor_command_response_manager import (
    ConnectionSupervisorCommandResponseManager,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_execute_connects_execution_with_response_manager():
    execution = Mock(
        spec=ConnectionSupervisorCommandExecution
    )
    response_manager = Mock(
        spec=ConnectionSupervisorCommandResponseManager
    )
    request = Mock(spec=ConnectionCommandRequest)
    result = Mock(spec=ConnectionCommandResult)

    execution.execute.return_value = result
    response_manager.process.return_value = "COMMAND_OK"

    integration = ConnectionSupervisorCommandResponseIntegration(
        execution,
        response_manager,
    )

    output = integration.execute(request)

    execution.execute.assert_called_once_with(request)
    response_manager.process.assert_called_once_with(result)
    assert output == "COMMAND_OK"


def test_execute_passes_blocked_result_to_response_manager():
    execution = Mock(
        spec=ConnectionSupervisorCommandExecution
    )
    response_manager = Mock(
        spec=ConnectionSupervisorCommandResponseManager
    )
    request = Mock(spec=ConnectionCommandRequest)

    execution.execute.return_value = None
    response_manager.process.return_value = "COMMAND_BLOCKED"

    integration = ConnectionSupervisorCommandResponseIntegration(
        execution,
        response_manager,
    )

    output = integration.execute(request)

    execution.execute.assert_called_once_with(request)
    response_manager.process.assert_called_once_with(None)
    assert output == "COMMAND_BLOCKED"

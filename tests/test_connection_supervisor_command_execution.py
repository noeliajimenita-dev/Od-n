from unittest.mock import Mock

from src.telegram.connection_supervisor_command_access import (
    ConnectionSupervisorCommandAccess,
)
from src.telegram.connection_supervisor_command_dispatcher import (
    ConnectionSupervisorCommandDispatcher,
)
from src.telegram.connection_supervisor_command_execution import (
    ConnectionSupervisorCommandExecution,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


def test_execute_dispatches_when_access_is_allowed():
    access = Mock(spec=ConnectionSupervisorCommandAccess)
    dispatcher = Mock(spec=ConnectionSupervisorCommandDispatcher)
    request = Mock(spec=ConnectionCommandRequest)
    expected_result = Mock(spec=ConnectionCommandResult)

    access.can_execute.return_value = True
    dispatcher.dispatch.return_value = expected_result

    execution = ConnectionSupervisorCommandExecution(
        access,
        dispatcher,
    )

    result = execution.execute(request)

    access.can_execute.assert_called_once_with(request)
    dispatcher.dispatch.assert_called_once_with(request)
    assert result is expected_result


def test_execute_blocks_when_access_is_denied():
    access = Mock(spec=ConnectionSupervisorCommandAccess)
    dispatcher = Mock(spec=ConnectionSupervisorCommandDispatcher)
    request = Mock(spec=ConnectionCommandRequest)

    access.can_execute.return_value = False

    execution = ConnectionSupervisorCommandExecution(
        access,
        dispatcher,
    )

    result = execution.execute(request)

    access.can_execute.assert_called_once_with(request)
    dispatcher.dispatch.assert_not_called()
    assert result is None

from unittest.mock import Mock

from src.telegram.connection_supervisor_command_audit_manager import (
    ConnectionSupervisorCommandAuditManager,
)
from src.telegram.connection_supervisor_command_dispatcher import (
    ConnectionSupervisorCommandDispatcher,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_commands import ConnectionCommandRequest


def test_dispatch_sends_request_to_audit_manager():
    audit_manager = Mock(spec=ConnectionSupervisorCommandAuditManager)
    expected_result = Mock(spec=ConnectionCommandResult)

    audit_manager.execute.return_value = expected_result

    dispatcher = ConnectionSupervisorCommandDispatcher(audit_manager)

    request = ConnectionCommandRequest(
        command="CONNECT",
        bot_name="bot_1",
    )

    result = dispatcher.dispatch(request)

    audit_manager.execute.assert_called_once_with(request)
    assert result is expected_result

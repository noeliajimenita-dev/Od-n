from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandSecurity:
    ALLOWED_COMMANDS = {
        "CONNECT",
        "DISCONNECT",
        "RECONNECT",
        "STATUS",
    }

    def is_allowed(
        self,
        request: ConnectionCommandRequest,
    ) -> bool:
        if request is None:
            return False

        command = getattr(request, "command", None)

        if command is None:
            return False

        command_value = getattr(command, "value", command)

        return str(command_value).upper() in self.ALLOWED_COMMANDS

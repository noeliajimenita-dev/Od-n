from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandValidation:
    def validate(
        self,
        request: ConnectionCommandRequest,
    ) -> bool:
        if request is None:
            return False

        if not getattr(request, "command", None):
            return False

        if not getattr(request, "bot_name", None):
            return False

        return True

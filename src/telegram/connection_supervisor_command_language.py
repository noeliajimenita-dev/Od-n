class ConnectionSupervisorCommandLanguage:
    COMMANDS = {
        "approved": "APPROVE",
        "genehmigt": "APPROVE",
        "aprobado": "APPROVE",
        "rejected": "REJECT",
        "declined": "REJECT",
        "abgelehnt": "REJECT",
        "abgewiesen": "REJECT",
        "redo": "REDO",
        "rework": "REDO",
        "überarbeiten": "REDO",
        "neu machen": "REDO",
        "pause": "PAUSE",
        "hold": "PAUSE",
        "stopp": "PAUSE",
        "pausar": "PAUSE",
        "resume": "RESUME",
        "back to normal": "RESUME",
        "weitermachen": "RESUME",
        "reanudar": "RESUME",
    }

    def normalize(self, command: str) -> str | None:
        if not command:
            return None

        normalized = " ".join(command.strip().lower().split())

        return self.COMMANDS.get(normalized)

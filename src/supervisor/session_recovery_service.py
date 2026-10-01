from src.supervisor.session_repository import SessionRepository
from src.supervisor.session_snapshot import SessionSnapshot
from src.supervisor.session_state import SessionState


class SessionRecoveryService:
    """Recovers Supervisor sessions from persisted snapshots."""

    def __init__(self, repository: SessionRepository):
        if repository is None:
            raise ValueError("Session repository is required")

        self.repository = repository

    def recover(self, snapshot: SessionSnapshot) -> SessionState:
        if not isinstance(snapshot, SessionSnapshot):
            raise TypeError("Expected a SessionSnapshot")

        session = snapshot.to_session()
        self.repository.save(session)
        return session

    def recover_from_dict(self, data: dict) -> SessionState:
        snapshot = SessionSnapshot.from_dict(data)
        return self.recover(snapshot)

    def recover_all(
        self,
        snapshots: list[SessionSnapshot],
    ) -> list[SessionState]:
        if snapshots is None:
            raise ValueError("Snapshots are required")

        recovered_sessions = []

        for snapshot in snapshots:
            recovered_sessions.append(self.recover(snapshot))

        return recovered_sessions

    def get_recovered(self, session_id: str) -> SessionState | None:
        return self.repository.get(session_id)

    def count_recovered(self) -> int:
        return self.repository.count()

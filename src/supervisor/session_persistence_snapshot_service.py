from src.supervisor.session_persistence_service import SessionPersistenceService
from src.supervisor.session_snapshot import SessionSnapshot
from src.supervisor.session_state import SessionState


class SessionPersistenceSnapshotService:
    """Coordinates creation and persistence of Supervisor session snapshots."""

    def __init__(self, persistence_service: SessionPersistenceService):
        if persistence_service is None:
            raise ValueError("Session persistence service is required")
        self.persistence_service = persistence_service

    def create_snapshot(self, session: SessionState) -> SessionSnapshot:
        if not isinstance(session, SessionState):
            raise TypeError("Expected a SessionState instance")

        return SessionSnapshot.from_session(session)

    def save_snapshot(self, snapshot: SessionSnapshot) -> SessionSnapshot:
        if not isinstance(snapshot, SessionSnapshot):
            raise TypeError("Expected a SessionSnapshot")

        session = snapshot.to_session()
        self.persistence_service.save(session)
        return snapshot

    def save_session_snapshot(self, session: SessionState) -> SessionSnapshot:
        snapshot = self.create_snapshot(session)
        return self.save_snapshot(snapshot)

    def get_snapshot(self, session_id: str) -> SessionSnapshot | None:
        session = self.persistence_service.get(session_id)

        if session is None:
            return None

        return SessionSnapshot.from_session(session)

    def list_snapshots(self) -> list[SessionSnapshot]:
        sessions = self.persistence_service.list_sessions()
        return [
            SessionSnapshot.from_session(session)
            for session in sessions
        ]

    def count_snapshots(self) -> int:
        return self.persistence_service.count()

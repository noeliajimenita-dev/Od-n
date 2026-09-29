from src.telegram.connection_session import TelegramConnectionSession
from src.telegram.connection_health import check_connection_health


def test_connected_session_is_healthy():
    session = TelegramConnectionSession(bot_name="worker_1")

    session.connect()

    health = check_connection_health(session)

    assert health.bot_name == "worker_1"
    assert health.healthy is True
    assert health.connected is True
    assert health.reason == "Conexión activa."


def test_disconnected_session_is_unhealthy():
    session = TelegramConnectionSession(bot_name="worker_1")

    health = check_connection_health(session)

    assert health.bot_name == "worker_1"
    assert health.healthy is False
    assert health.connected is False
    assert health.reason == "El bot no está conectado."

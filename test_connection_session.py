from src.telegram.connection_session import TelegramConnectionSession


def test_session_starts_disconnected():
    session = TelegramConnectionSession(bot_name="test_bot")

    assert session.is_connected() is False
    assert session.connected_at is None


def test_session_connects():
    session = TelegramConnectionSession(bot_name="test_bot")

    session.connect()

    assert session.is_connected() is True
    assert session.connected_at is not None


def test_session_disconnects():
    session = TelegramConnectionSession(bot_name="test_bot")

    session.connect()
    session.disconnect()

    assert session.is_connected() is False
    assert session.connected_at is None


def test_repeated_connect_does_not_change_connection_time():
    session = TelegramConnectionSession(bot_name="test_bot")

    session.connect()
    first_connection_time = session.connected_at

    session.connect()

    assert session.connected_at == first_connection_time

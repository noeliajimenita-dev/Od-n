from src.telegram.bot_registry_status import get_bot_registry_status


def test_bot_registry_status_returns_six_bots(monkeypatch):
    def fake_load_token(env_variable):
        return "test-token"

    monkeypatch.setattr(
        "src.telegram.bot_registry_status.load_bot_token",
        fake_load_token,
    )

    statuses = get_bot_registry_status()

    assert len(statuses) == 6
    assert all(status.token_configured for status in statuses)


def test_bot_registry_status_without_tokens(monkeypatch):
    def fake_load_token(env_variable):
        raise ValueError("Token no configurado")

    monkeypatch.setattr(
        "src.telegram.bot_registry_status.load_bot_token",
        fake_load_token,
    )

    statuses = get_bot_registry_status()

    assert len(statuses) == 6
    assert all(not status.token_configured for status in statuses)

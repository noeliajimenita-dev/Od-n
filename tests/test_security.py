from src.config.security import (
    get_missing_credentials,
    has_any_credentials,
    credentials_are_hidden,
)


def test_missing_credentials_returns_list():
    result = get_missing_credentials()

    assert isinstance(result, list)


def test_missing_credentials_contains_only_names():
    result = get_missing_credentials()

    for name in result:
        assert isinstance(name, str)
        assert "KEY" in name or "TOKEN" in name


def test_has_any_credentials_returns_boolean():
    result = has_any_credentials()

    assert isinstance(result, bool)


def test_credentials_are_hidden():
    assert credentials_are_hidden() is True

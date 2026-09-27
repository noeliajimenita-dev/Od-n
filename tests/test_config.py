from src.config.validation import (
    validate_configuration,
    configuration_is_valid,
)


def test_configuration_returns_list():
    errors = validate_configuration()

    assert isinstance(errors, list)


def test_configuration_is_valid_returns_boolean():
    result = configuration_is_valid()

    assert isinstance(result, bool)


def test_invalid_environment_is_detected(monkeypatch):
    monkeypatch.setenv(
        "APP_ENV",
        "invalid_environment"
    )

    # Recargar el módulo para utilizar el nuevo valor.
    import importlib
    import src.config.settings as settings
    import src.config.validation as validation

    importlib.reload(settings)
    importlib.reload(validation)

    errors = validation.validate_configuration()

    assert any(
        "APP_ENV inválido" in error
        for error in errors
    )


def test_negative_daily_limit_is_detected(monkeypatch):
    monkeypatch.setenv(
        "DAILY_TOKEN_LIMIT",
        "-1"
    )

    import importlib
    import src.config.settings as settings
    import src.config.validation as validation

    importlib.reload(settings)
    importlib.reload(validation)

    errors = validation.validate_configuration()

    assert any(
        "DAILY_TOKEN_LIMIT" in error
        for error in errors
    )

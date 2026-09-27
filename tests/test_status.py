from src.config.status import (
    get_configuration_status,
    is_ready_for_execution,
)


def test_configuration_status_returns_dictionary():
    status = get_configuration_status()

    assert isinstance(status, dict)


def test_configuration_status_contains_basic_information():
    status = get_configuration_status()

    assert "app_name" in status
    assert "environment" in status
    assert "version" in status
    assert "configuration_valid" in status
    assert "configuration_errors" in status
    assert "missing_credentials" in status


def test_configuration_status_does_not_contain_secret_values():
    status = get_configuration_status()

    assert isinstance(status["missing_credentials"], list)

    for credential in status["missing_credentials"]:
        assert isinstance(credential, str)


def test_execution_readiness_returns_boolean():
    result = is_ready_for_execution()

    assert isinstance(result, bool)

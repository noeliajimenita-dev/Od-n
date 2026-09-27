from src.config.constants import (
    ENV_DEVELOPMENT,
    ENV_TESTING,
    ENV_PRODUCTION,
)


def test_environment_names():
    assert ENV_DEVELOPMENT == "development"
    assert ENV_TESTING == "testing"
    assert ENV_PRODUCTION == "production"


def test_environments_are_unique():
    environments = [
        ENV_DEVELOPMENT,
        ENV_TESTING,
        ENV_PRODUCTION,
    ]

    assert len(set(environments)) == 3


def test_environments_are_strings():
    environments = [
        ENV_DEVELOPMENT,
        ENV_TESTING,
        ENV_PRODUCTION,
    ]

    assert all(
        isinstance(environment, str)
        for environment in environments
    )

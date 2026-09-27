from src.config.constants import (
    PROJECT_NAME,
    DEFAULT_VERSION,
    PROVIDER_GEMINI,
    PROVIDER_GROQ,
    ROLE_SUPERVISOR,
    WORKER_1,
    WORKER_2,
    WORKER_3,
    WORKER_4,
    WORKER_5,
    TASK_PENDING,
    TASK_WORKING,
    TASK_COMPLETED,
    TASK_FAILED,
    ACTION_ALLOWED,
    ACTION_REQUIRES_APPROVAL,
    ACTION_DENIED,
    RESOURCE_AVAILABLE,
    RESOURCE_LIMIT,
    RESOURCE_ERROR,
    COMMAND_STOP_ALL,
    COMMAND_PAUSE,
    COMMAND_RESUME,
)


def test_project_information():
    assert PROJECT_NAME == "THE ODIN PROJECT"
    assert DEFAULT_VERSION == "0.1.0"


def test_ai_providers():
    assert PROVIDER_GEMINI == "gemini"
    assert PROVIDER_GROQ == "groq"


def test_bot_roles():
    assert ROLE_SUPERVISOR == "supervisor"

    workers = [
        WORKER_1,
        WORKER_2,
        WORKER_3,
        WORKER_4,
        WORKER_5,
    ]

    assert len(workers) == 5
    assert len(set(workers)) == 5


def test_task_states():
    states = [
        TASK_PENDING,
        TASK_WORKING,
        TASK_COMPLETED,
        TASK_FAILED,
    ]

    assert all(isinstance(state, str) for state in states)
    assert len(set(states)) == len(states)


def test_action_permissions():
    permissions = [
        ACTION_ALLOWED,
        ACTION_REQUIRES_APPROVAL,
        ACTION_DENIED,
    ]

    assert len(set(permissions)) == 3


def test_resource_states():
    states = [
        RESOURCE_AVAILABLE,
        RESOURCE_LIMIT,
        RESOURCE_ERROR,
    ]

    assert len(set(states)) == 3


def test_control_commands():
    commands = [
        COMMAND_STOP_ALL,
        COMMAND_PAUSE,
        COMMAND_RESUME,
    ]

    assert "STOP ALL" in commands
    assert "PAUSE" in commands
    assert "RESUME" in commands

from pathlib import Path

from src.config.paths import (
    PROJECT_ROOT,
    SRC_DIR,
    TESTS_DIR,
    DOCS_DIR,
    DATA_DIR,
    RUNTIME_DIR,
    LOCAL_DATA_DIR,
    LOGS_DIR,
    TEMP_DIR,
    SECRETS_DIR,
    GENERATED_DIR,
    get_project_root,
)


def test_project_root_is_path():
    assert isinstance(PROJECT_ROOT, Path)


def test_project_root_function():
    assert get_project_root() == PROJECT_ROOT


def test_main_directories_are_inside_project():
    directories = [
        SRC_DIR,
        TESTS_DIR,
        DOCS_DIR,
        DATA_DIR,
        RUNTIME_DIR,
        LOCAL_DATA_DIR,
        LOGS_DIR,
        TEMP_DIR,
        SECRETS_DIR,
        GENERATED_DIR,
    ]

    for directory in directories:
        assert PROJECT_ROOT in directory.parents or directory == PROJECT_ROOT


def test_runtime_directory_is_inside_data():
    assert DATA_DIR in RUNTIME_DIR.parents


def test_local_data_directory_is_inside_data():
    assert DATA_DIR in LOCAL_DATA_DIR.parents

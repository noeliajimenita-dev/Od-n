from unittest.mock import Mock

from src.telegram.connection_supervisor_command_language import (
    ConnectionSupervisorCommandLanguage,
)
from src.telegram.connection_supervisor_command_parser import (
    ConnectionSupervisorCommandParser,
)


def test_parse_delegates_message_to_language_normalizer():
    language = Mock(
        spec=ConnectionSupervisorCommandLanguage
    )

    language.normalize.return_value = "APPROVE"

    parser = ConnectionSupervisorCommandParser(language)

    result = parser.parse("Genehmigt")

    language.normalize.assert_called_once_with("Genehmigt")
    assert result == "APPROVE"


def test_parse_returns_redo_command():
    language = Mock(
        spec=ConnectionSupervisorCommandLanguage
    )

    language.normalize.return_value = "REDO"

    parser = ConnectionSupervisorCommandParser(language)

    result = parser.parse("Rework")

    language.normalize.assert_called_once_with("Rework")
    assert result == "REDO"


def test_parse_returns_pause_command():
    language = Mock(
        spec=ConnectionSupervisorCommandLanguage
    )

    language.normalize.return_value = "PAUSE"

    parser = ConnectionSupervisorCommandParser(language)

    result = parser.parse("Stopp")

    language.normalize.assert_called_once_with("Stopp")
    assert result == "PAUSE"


def test_parse_returns_none_for_unknown_message():
    language = Mock(
        spec=ConnectionSupervisorCommandLanguage
    )

    language.normalize.return_value = None

    parser = ConnectionSupervisorCommandParser(language)

    result = parser.parse("unknown command")

    language.normalize.assert_called_once_with("unknown command")
    assert result is None

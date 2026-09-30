from src.telegram.connection_supervisor_command_language import (
    ConnectionSupervisorCommandLanguage,
)


def test_normalize_approved_in_multiple_languages():
    language = ConnectionSupervisorCommandLanguage()

    assert language.normalize("Approved") == "APPROVE"
    assert language.normalize("Aprobado") == "APPROVE"
    assert language.normalize("Genehmigt") == "APPROVE"


def test_normalize_rejected_in_multiple_languages():
    language = ConnectionSupervisorCommandLanguage()

    assert language.normalize("Rejected") == "REJECT"
    assert language.normalize("Declined") == "REJECT"
    assert language.normalize("Abgelehnt") == "REJECT"


def test_normalize_redo_in_multiple_languages():
    language = ConnectionSupervisorCommandLanguage()

    assert language.normalize("Redo") == "REDO"
    assert language.normalize("Rework") == "REDO"
    assert language.normalize("Überarbeiten") == "REDO"


def test_normalize_pause_in_multiple_languages():
    language = ConnectionSupervisorCommandLanguage()

    assert language.normalize("Pause") == "PAUSE"
    assert language.normalize("Hold") == "PAUSE"
    assert language.normalize("Stopp") == "PAUSE"


def test_normalize_resume_in_multiple_languages():
    language = ConnectionSupervisorCommandLanguage()

    assert language.normalize("Resume") == "RESUME"
    assert language.normalize("Back to normal") == "RESUME"
    assert language.normalize("Weitermachen") == "RESUME"


def test_normalize_unknown_command_returns_none():
    language = ConnectionSupervisorCommandLanguage()

    assert language.normalize("something unknown") is None


def test_normalize_empty_command_returns_none():
    language = ConnectionSupervisorCommandLanguage()

    assert language.normalize("") is None
    assert language.normalize(None) is None

import pytest

from src.worker_4.skills import DEFAULT_SKILLS, Worker4Skills


def test_worker_has_default_skills():
    skills = Worker4Skills()

    assert skills.all_skills() == DEFAULT_SKILLS
    assert len(skills.all_skills()) == 15


def test_has_skill_returns_true_for_existing_skill():
    skills = Worker4Skills()

    assert skills.has_skill("data_analysis") is True


def test_has_skill_returns_false_for_missing_skill():
    skills = Worker4Skills()

    assert skills.has_skill("unknown_skill") is False


def test_add_skill():
    skills = Worker4Skills()

    skills.add_skill("custom_skill")

    assert skills.has_skill("custom_skill") is True


def test_add_skill_does_not_duplicate():
    skills = Worker4Skills()

    skills.add_skill("custom_skill")
    skills.add_skill("custom_skill")

    assert skills.all_skills().count("custom_skill") == 1


def test_add_empty_skill_fails():
    skills = Worker4Skills()

    with pytest.raises(ValueError):
        skills.add_skill("   ")


def test_remove_skill():
    skills = Worker4Skills()

    skills.add_skill("custom_skill")
    skills.remove_skill("custom_skill")

    assert skills.has_skill("custom_skill") is False


def test_remove_missing_skill_is_safe():
    skills = Worker4Skills()

    skills.remove_skill("unknown_skill")

    assert skills.all_skills() == DEFAULT_SKILLS


def test_all_skills_returns_copy():
    skills = Worker4Skills()

    result = skills.all_skills()
    result.append("temporary_skill")

    assert skills.has_skill("temporary_skill") is False

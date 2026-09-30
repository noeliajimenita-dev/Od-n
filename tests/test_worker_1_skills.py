from src.worker_1.skills import DEFAULT_SKILLS, Worker1Skills


def test_worker_has_15_default_skills():
    skills = Worker1Skills()

    assert len(skills.all_skills()) == 15


def test_default_skills_match_expected_skills():
    skills = Worker1Skills()

    assert skills.all_skills() == DEFAULT_SKILLS


def test_has_skill():
    skills = Worker1Skills()

    assert skills.has_skill("machine_learning") is True
    assert skills.has_skill("data_analysis") is True


def test_missing_skill_returns_false():
    skills = Worker1Skills()

    assert skills.has_skill("unknown_skill") is False


def test_add_skill():
    skills = Worker1Skills([])

    skills.add_skill("custom_skill")

    assert skills.has_skill("custom_skill") is True


def test_add_skill_does_not_duplicate():
    skills = Worker1Skills([])

    skills.add_skill("custom_skill")
    skills.add_skill("custom_skill")

    assert skills.all_skills() == ["custom_skill"]


def test_add_empty_skill_fails():
    skills = Worker1Skills([])

    try:
        skills.add_skill("   ")
        assert False
    except ValueError:
        assert True


def test_remove_skill():
    skills = Worker1Skills(["custom_skill"])

    skills.remove_skill("custom_skill")

    assert skills.has_skill("custom_skill") is False


def test_remove_missing_skill_is_safe():
    skills = Worker1Skills([])

    skills.remove_skill("unknown_skill")

    assert skills.all_skills() == []


def test_all_skills_returns_copy():
    skills = Worker1Skills(["custom_skill"])

    result = skills.all_skills()
    result.append("another_skill")

    assert skills.all_skills() == ["custom_skill"]

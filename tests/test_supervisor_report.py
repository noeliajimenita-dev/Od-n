from src.supervisor.supervisor_report import SupervisorReport


class FakeTask:
    def __init__(self, status):
        self.status = status


def test_report_classifies_tasks():
    report = SupervisorReport()

    tasks = {
        "task-001": FakeTask("completed"),
        "task-002": FakeTask("failed"),
        "task-003": FakeTask("running"),
        "task-004": FakeTask("pending"),
    }

    result = report.generate(tasks)

    assert result["total_tasks"] == 4
    assert result["completed"] == ["task-001"]
    assert result["failed"] == ["task-002"]
    assert result["active"] == ["task-003", "task-004"]


def test_report_with_no_tasks():
    report = SupervisorReport()

    result = report.generate({})

    assert result["total_tasks"] == 0
    assert result["completed"] == []
    assert result["failed"] == []
    assert result["active"] == []

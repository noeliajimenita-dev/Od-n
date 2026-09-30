from src.supervisor.supervisor import Supervisor


class FakeDispatcher:
    def dispatch(self, task):
        return {
            "id": task["id"],
            "assigned": True,
        }


class FakeExecutor:
    def execute(self, task):
        return {
            "task_id": task["id"],
            "result": "completed",
        }


def test_supervisor_registers_task():
    supervisor = Supervisor()

    task = {
        "id": "task-001",
        "description": "Test task",
    }

    supervisor.register_task("task-001", task)

    assert "task-001" in supervisor.active_tasks
    assert supervisor.active_tasks["task-001"] == task


def test_supervisor_executes_task():
    supervisor = Supervisor(
        dispatcher=FakeDispatcher(),
        executor=FakeExecutor(),
    )

    supervisor.register_task(
        "task-001",
        {
            "id": "task-001",
            "description": "Test task",
        },
    )

    result = supervisor.execute("task-001")

    assert result.task_id == "task-001"
    assert result.status == "completed"
    assert result.result["task_id"] == "task-001"


def test_supervisor_handles_missing_task():
    supervisor = Supervisor()

    result = supervisor.execute("unknown-task")

    assert result.task_id == "unknown-task"
    assert result.status == "error"
    assert result.error == "Task not found"


def test_supervisor_reports_status():
    supervisor = Supervisor()

    supervisor.register_task("task-001", {"id": "task-001"})
    supervisor.register_task("task-002", {"id": "task-002"})

    status = supervisor.get_status()

    assert status["active_tasks"] == 2
    assert status["task_ids"] == ["task-001", "task-002"]

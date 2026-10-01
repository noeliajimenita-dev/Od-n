from typing import Any


class TaskAssignmentMonitor:
    """Monitors the state of Supervisor task assignments."""

    def get_status(self, tasks: dict[str, Any]) -> dict[str, Any]:
        assigned = []
        running = []
        completed = []
        failed = []
        pending = []

        for task_id, task in tasks.items():
            status = getattr(task, "status", "unknown")

            if status == "assigned":
                assigned.append(task_id)
            elif status == "running":
                running.append(task_id)
            elif status == "completed":
                completed.append(task_id)
            elif status == "failed":
                failed.append(task_id)
            elif status == "pending":
                pending.append(task_id)

        return {
            "total": len(tasks),
            "assigned": assigned,
            "running": running,
            "completed": completed,
            "failed": failed,
            "pending": pending,
        }

    def active_tasks(self, tasks: dict[str, Any]) -> list[str]:
        status = self.get_status(tasks)

        return status["assigned"] + status["running"]

    def completed_tasks(self, tasks: dict[str, Any]) -> list[str]:
        return self.get_status(tasks)["completed"]

    def failed_tasks(self, tasks: dict[str, Any]) -> list[str]:
        return self.get_status(tasks)["failed"]

    def has_active_tasks(self, tasks: dict[str, Any]) -> bool:
        return bool(self.active_tasks(tasks))

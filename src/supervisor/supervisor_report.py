from typing import Any


class SupervisorReport:
    def generate(
        self,
        tasks: dict[str, Any],
    ) -> dict[str, Any]:
        completed = []
        failed = []
        active = []

        for task_id, task in tasks.items():
            status = getattr(task, "status", "unknown")

            if status == "completed":
                completed.append(task_id)
            elif status == "failed":
                failed.append(task_id)
            else:
                active.append(task_id)

        return {
            "total_tasks": len(tasks),
            "completed": completed,
            "failed": failed,
            "active": active,
        }

from src.supervisor.task import Task
from src.supervisor.worker_bridge import SupervisorWorkerBridge


class SupervisorTaskRouter:
    """Routes Supervisor tasks through the worker bridge."""

    def __init__(self, bridge: SupervisorWorkerBridge):
        if bridge is None:
            raise ValueError("Supervisor worker bridge is required")

        self.bridge = bridge

    def route(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        required_skill = task.metadata.get("required_skill")

        return self.bridge.assign_task(
            task,
            required_skill=required_skill,
        )

    def route_with_skill(self, task: Task, skill: str):
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if not skill or not skill.strip():
            raise ValueError("Skill cannot be empty")

        task.metadata["required_skill"] = skill.strip().lower()

        return self.bridge.assign_task(
            task,
            required_skill=task.metadata["required_skill"],
        )

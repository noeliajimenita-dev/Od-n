from .task import Task


class TaskAnalyzer:
    def analyze(
        self,
        task_id: str,
        instruction: str,
        priority: int = 0,
    ) -> Task:
        if not instruction or not instruction.strip():
            raise ValueError("Task instruction cannot be empty")

        normalized_instruction = " ".join(
            instruction.strip().split()
        )

        return Task(
            task_id=task_id,
            description=normalized_instruction,
            priority=priority,
            metadata={
                "source": "supervisor",
                "analyzed": True,
            },
        )

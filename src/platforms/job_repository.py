from __future__ import annotations

from .job import Job


class JobRepository:
    """Repositorio en memoria de oportunidades de trabajo."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}

    def save(self, job: Job) -> Job:
        if job is None:
            raise ValueError("job cannot be None")

        self._jobs[job.job_id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        if not job_id or not job_id.strip():
            return None

        return self._jobs.get(job_id)

    def exists(self, job_id: str) -> bool:
        return self.get(job_id) is not None

    def delete(self, job_id: str) -> bool:
        if job_id not in self._jobs:
            return False

        del self._jobs[job_id]
        return True

    def list_all(self) -> list[Job]:
        return list(self._jobs.values())

    def list_by_platform(
        self,
        platform: str,
    ) -> list[Job]:
        platform = platform.strip().lower()

        return [
            job
            for job in self._jobs.values()
            if job.platform.lower() == platform
        ]

    def list_by_status(
        self,
        status: str,
    ) -> list[Job]:
        status = status.strip().lower()

        return [
            job
            for job in self._jobs.values()
            if job.status.lower() == status
        ]

    def list_by_skill(
        self,
        skill: str,
    ) -> list[Job]:
        skill = skill.strip().lower()

        return [
            job
            for job in self._jobs.values()
            if job.requires_skill(skill)
        ]

    def list_by_price_range(
        self,
        minimum: float = 0.0,
        maximum: float | None = None,
    ) -> list[Job]:
        if minimum < 0:
            raise ValueError(
                "minimum cannot be negative"
            )

        if maximum is not None and maximum < minimum:
            raise ValueError(
                "maximum cannot be lower than minimum"
            )

        return [
            job
            for job in self._jobs.values()
            if job.price >= minimum
            and (
                maximum is None
                or job.price <= maximum
            )
        ]

    def count(self) -> int:
        return len(self._jobs)

    def count_by_status(self, status: str) -> int:
        return len(self.list_by_status(status))

    def clear(self) -> None:
        self._jobs.clear()

    def __repr__(self) -> str:
        return (
            "JobRepository("
            f"jobs={self.count()}"
            ")"
          )

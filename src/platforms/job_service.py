from __future__ import annotations

from .job import Job
from .job_repository import JobRepository


class JobService:
    """Servicio central para gestionar oportunidades externas."""

    def __init__(self, repository: JobRepository) -> None:
        if repository is None:
            raise ValueError("repository cannot be None")

        self.repository = repository

    def add(self, job: Job) -> Job:
        if job is None:
            raise ValueError("job cannot be None")

        if self.repository.exists(job.job_id):
            raise ValueError(
                f"Job already exists: {job.job_id}"
            )

        return self.repository.save(job)

    def get(self, job_id: str) -> Job | None:
        return self.repository.get(job_id)

    def review(self, job_id: str) -> Job:
        job = self._require(job_id)
        job.mark_reviewing()
        return self.repository.save(job)

    def evaluate(
        self,
        job_id: str,
        required_skills: set[str] | None = None,
        minimum_price: float = 0.0,
        maximum_price: float | None = None,
    ) -> bool:
        job = self._require(job_id)

        if minimum_price < 0:
            raise ValueError(
                "minimum_price cannot be negative"
            )

        if (
            maximum_price is not None
            and maximum_price < minimum_price
        ):
            raise ValueError(
                "maximum_price cannot be lower "
                "than minimum_price"
            )

        if job.price < minimum_price:
            job.mark_discarded()
            self.repository.save(job)
            return False

        if (
            maximum_price is not None
            and job.price > maximum_price
        ):
            job.mark_discarded()
            self.repository.save(job)
            return False

        if required_skills:
            normalized = {
                skill.strip().lower()
                for skill in required_skills
                if skill.strip()
            }

            if not normalized.issubset(
                job.required_skills
            ):
                job.mark_discarded()
                self.repository.save(job)
                return False

        job.mark_eligible()
        self.repository.save(job)
        return True

    def apply_mark(
        self,
        job_id: str,
    ) -> Job:
        job = self._require(job_id)

        if not job.is_eligible():
            raise ValueError(
                "Job must be eligible before applying"
            )

        job.mark_applied()
        return self.repository.save(job)

    def complete(
        self,
        job_id: str,
    ) -> Job:
        job = self._require(job_id)
        job.mark_completed()
        return self.repository.save(job)

    def list_active(self) -> list[Job]:
        return [
            job
            for job in self.repository.list_all()
            if job.is_active()
        ]

    def list_eligible(self) -> list[Job]:
        return self.repository.list_by_status(
            "eligible"
        )

    def list_by_platform(
        self,
        platform: str,
    ) -> list[Job]:
        return self.repository.list_by_platform(platform)

    def list_by_skill(
        self,
        skill: str,
    ) -> list[Job]:
        return self.repository.list_by_skill(skill)

    def remove(self, job_id: str) -> bool:
        return self.repository.delete(job_id)

    def count(self) -> int:
        return self.repository.count()

    def _require(self, job_id: str) -> Job:
        job = self.get(job_id)

        if job is None:
            raise ValueError(
                f"Job not found: {job_id}"
            )

        return job

    def __repr__(self) -> str:
        return (
            "JobService("
            f"jobs={self.count()}, "
            f"eligible={len(self.list_eligible())}"
            ")"
  )

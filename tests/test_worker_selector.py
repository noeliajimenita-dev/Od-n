from src.workers.worker_selector import WorkerSelector


class MockWorker:
    def __init__(self, status="idle", skills=None):
        self.status = status
        self.skills = skills or []

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills


def test_selector_returns_none_when_no_workers():
    selector = WorkerSelector()

    result = selector.select({})

    assert result is None


def test_selector_returns_available_worker():
    selector = WorkerSelector()
    worker = MockWorker()

    result = selector.select({"worker_1": worker})

    assert result is worker


def test_selector_skips_busy_worker():
    selector = WorkerSelector()

    busy_worker = MockWorker(status="working")
    idle_worker = MockWorker(status="idle")

    result = selector.select(
        {
            "worker_1": busy_worker,
            "worker_2": idle_worker,
        }
    )

    assert result is idle_worker


def test_selector_returns_none_when_all_workers_are_busy():
    selector = WorkerSelector()

    workers = {
        "worker_1": MockWorker(status="working"),
        "worker_2": MockWorker(status="paused"),
    }

    result = selector.select(workers)

    assert result is None


def test_selector_matches_required_skill():
    selector = WorkerSelector()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    result = selector.select(
        {
            "worker_1": worker_1,
            "worker_2": worker_2,
        },
        required_skill="cybersecurity",
    )

    assert result is worker_2


def test_selector_skips_available_worker_without_required_skill():
    selector = WorkerSelector()

    worker_1 = MockWorker(skills=["data_science"])
    worker_2 = MockWorker(skills=["cybersecurity"])

    result = selector.select(
        {
            "worker_1": worker_1,
            "worker_2": worker_2,
        },
        required_skill="cybersecurity",
    )

    assert result is worker_2


def test_selector_returns_none_when_skill_is_unavailable():
    selector = WorkerSelector()

    workers = {
        "worker_1": MockWorker(skills=["data_science"]),
        "worker_2": MockWorker(skills=["cybersecurity"]),
    }

    result = selector.select(
        workers,
        required_skill="graphic_design",
    )

    assert result is None


def test_selector_skips_busy_worker_with_matching_skill():
    selector = WorkerSelector()

    busy_worker = MockWorker(
        status="working",
        skills=["cybersecurity"],
    )
    idle_worker = MockWorker(
        status="idle",
        skills=["data_science"],
    )

    result = selector.select(
        {
            "worker_1": busy_worker,
            "worker_2": idle_worker,
        },
        required_skill="cybersecurity",
    )

    assert result is None

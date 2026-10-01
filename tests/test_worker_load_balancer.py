from src.workers.worker_load_balancer import WorkerLoadBalancer


class MockWorker:
    def __init__(
        self,
        status="idle",
        skills=None,
        pending_tasks=None,
        current_task=None,
    ):
        self.status = status
        self.skills = skills or []
        self.pending_tasks = pending_tasks or []
        self.current_task = current_task

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills


def test_balancer_returns_none_when_no_workers():
    balancer = WorkerLoadBalancer()

    result = balancer.select({})

    assert result is None


def test_balancer_selects_available_worker():
    balancer = WorkerLoadBalancer()
    worker = MockWorker()

    result = balancer.select({"worker_1": worker})

    assert result is worker


def test_balancer_skips_busy_workers():
    balancer = WorkerLoadBalancer()

    busy_worker = MockWorker(status="working")
    idle_worker = MockWorker(status="idle")

    result = balancer.select(
        {
            "worker_1": busy_worker,
            "worker_2": idle_worker,
        }
    )

    assert result is idle_worker


def test_balancer_selects_worker_with_fewest_pending_tasks():
    balancer = WorkerLoadBalancer()

    worker_1 = MockWorker(
        pending_tasks=["task-1", "task-2"],
    )
    worker_2 = MockWorker(
        pending_tasks=["task-3"],
    )

    result = balancer.select(
        {
            "worker_1": worker_1,
            "worker_2": worker_2,
        }
    )

    assert result is worker_2


def test_balancer_selects_worker_with_zero_pending_tasks():
    balancer = WorkerLoadBalancer()

    worker_1 = MockWorker(
        pending_tasks=["task-1"],
    )
    worker_2 = MockWorker(
        pending_tasks=[],
    )

    result = balancer.select(
        {
            "worker_1": worker_1,
            "worker_2": worker_2,
        }
    )

    assert result is worker_2


def test_balancer_filters_by_required_skill():
    balancer = WorkerLoadBalancer()

    worker_1 = MockWorker(
        skills=["data_science"],
        pending_tasks=[],
    )
    worker_2 = MockWorker(
        skills=["cybersecurity"],
        pending_tasks=["task-1"],
    )

    result = balancer.select(
        {
            "worker_1": worker_1,
            "worker_2": worker_2,
        },
        required_skill="cybersecurity",
    )

    assert result is worker_2


def test_balancer_returns_none_when_skill_is_unavailable():
    balancer = WorkerLoadBalancer()

    workers = {
        "worker_1": MockWorker(skills=["data_science"]),
        "worker_2": MockWorker(skills=["cybersecurity"]),
    }

    result = balancer.select(
        workers,
        required_skill="graphic_design",
    )

    assert result is None


def test_balancer_skips_busy_worker_even_with_required_skill():
    balancer = WorkerLoadBalancer()

    busy_worker = MockWorker(
        status="working",
        skills=["cybersecurity"],
    )
    idle_worker = MockWorker(
        status="idle",
        skills=["data_science"],
    )

    result = balancer.select(
        {
            "worker_1": busy_worker,
            "worker_2": idle_worker,
        },
        required_skill="cybersecurity",
    )

    assert result is None


def test_balancer_uses_current_task_when_pending_tasks_are_not_available():
    balancer = WorkerLoadBalancer()

    worker_1 = MockWorker(
        pending_tasks=[],
        current_task="task-1",
    )
    worker_2 = MockWorker(
        pending_tasks=[],
        current_task=None,
    )

    result = balancer.select(
        {
            "worker_1": worker_1,
            "worker_2": worker_2,
        }
    )

    assert result is worker_2

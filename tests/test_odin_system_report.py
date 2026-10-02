from __future__ import annotations

from src.integration.odin_system import OdinSystem
from src.integration.odin_system_report import OdinSystemReport


class Runtime:
    def status(self, current_datetime=None):
        return {
            "state": "running",
            "worker_count": 5,
        }


class Logs:
    def summary(self):
        return {"events": 10}

    def export(self):
        return {"events": 10}


class Backups:
    def status(self):
        return {
            "count": 3,
            "latest_version": "1.0.0",
        }


class Recovery:
    def status(self):
        return {
            "state": "ready",
        }


class Execution:
    def execute(self, task):
        return {"success": True}


class PlatformManager:
    def list_platforms(self):
        return [
            "upwork",
            "computrabajo",
            "linkedin",
            "fiverr",
            "workana",
        ]


def build_system() -> OdinSystem:
    return OdinSystem(
        runtime=Runtime(),
        logs=Logs(),
        backups=Backups(),
        recovery=Recovery(),
        execution_service=Execution(),
        platform_manager=PlatformManager(),
    )


def test_report_contains_system_information() -> None:
    system = build_system()
    report_service = OdinSystemReport()

    report = report_service.generate(system)

    assert report["system"] == "ODIN"
    assert "timestamp" in report
    assert "healthy" in report
    assert "ready" in report
    assert "validation" in report
    assert "health" in report
    assert "runtime" in report
    assert "backups" in report
    assert "recovery" in report
    assert "platforms" in report
    assert "components" in report


def test_report_detects_execution_component() -> None:
    system = build_system()
    report_service = OdinSystemReport()

    report = report_service.generate(system)

    assert report["components"]["execution"] is True


def test_report_lists_platforms() -> None:
    system = build_system()
    report_service = OdinSystemReport()

    report = report_service.generate(system)

    assert len(report["platforms"]) == 5
    assert "upwork" in report["platforms"]


def test_report_summary_contains_main_status() -> None:
    system = build_system()
    report_service = OdinSystemReport()

    summary = report_service.summary(system)

    assert "ODIN SYSTEM REPORT" in summary
    assert "Healthy:" in summary
    assert "Ready:" in summary
    assert "Validation:" in summary
    assert "Health:" in summary
    assert "Execution:" in summary


def test_secret_fields_are_redacted() -> None:
    system = build_system()

    system.runtime.status = lambda current_datetime=None: {
        "state": "running",
        "api_key": "SUPER_SECRET_KEY",
        "password": "SUPER_SECRET_PASSWORD",
        "token": "SUPER_SECRET_TOKEN",
        "nested": {
            "credential": "SECRET_CREDENTIAL",
        },
    }

    report_service = OdinSystemReport()
    report = report_service.generate(system)

    runtime = report["runtime"]

    assert runtime["api_key"] == "[REDACTED]"
    assert runtime["password"] == "[REDACTED]"
    assert runtime["token"] == "[REDACTED]"

    assert (
        runtime["nested"]["credential"]
        == "[REDACTED]"
    )


def test_private_key_is_redacted() -> None:
    system = build_system()

    system.runtime.status = lambda current_datetime=None: {
        "private_key": "PRIVATE_KEY_CONTENT",
        "state": "running",
    }

    report_service = OdinSystemReport()
    report = report_service.generate(system)

    assert (
        report["runtime"]["private_key"]
        == "[REDACTED]"
    )


def test_normal_values_are_preserved() -> None:
    system = build_system()

    system.runtime.status = lambda current_datetime=None: {
        "state": "running",
        "worker_count": 5,
        "active": True,
    }

    report_service = OdinSystemReport()
    report = report_service.generate(system)

    assert report["runtime"]["state"] == "running"
    assert report["runtime"]["worker_count"] == 5
    assert report["runtime"]["active"] is True


def test_nested_lists_are_processed_safely() -> None:
    system = build_system()

    system.runtime.status = lambda current_datetime=None: {
        "workers": [
            {
                "worker_id": "worker-1",
                "token": "SECRET",
            },
            {
                "worker_id": "worker-2",
                "status": "idle",
            },
        ]
    }

    report_service = OdinSystemReport()
    report = report_service.generate(system)

    workers = report["runtime"]["workers"]

    assert workers[0]["worker_id"] == "worker-1"
    assert workers[0]["token"] == "[REDACTED]"
    assert workers[1]["status"] == "idle"


def test_report_can_be_generated_without_optional_ai() -> None:
    system = build_system()
    system.ai_service = None

    report_service = OdinSystemReport()
    report

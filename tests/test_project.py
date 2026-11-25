
import pytest
from pydantic import ValidationError

from src.schemas import SpecArtifact, CodeArtifact, QAReport
from src.sandbox import run_tests
from src import orchestrator


def test_passing_code():
    result = run_tests(
        "def add(a, b): return a + b",
        "from implementation import add\n"
        "def test_add(): assert add(2, 3) == 5"
    )
    assert result["exit_code"] == 0


def test_failing_code():
    result = run_tests(
        "def add(a, b): return a + b",
        "from implementation import add\n"
        "def test_add(): assert add(2, 3) == 10"
    )
    assert result["exit_code"] != 0
    assert "failed" in result["stdout"].lower()


def test_timeout():
    result = run_tests(
        "def hello(): return 'hello'",
        "import time\n"
        "def test_slow(): time.sleep(12)"
    )
    assert result["timed_out"] is True


def test_schema_validation():
    spec = SpecArtifact(
        feature_name="Add numbers",
        requirements=["Add two numbers"],
        test_cases=["Test 2 + 3"],
        interfaces=["add(a, b)"]
    )
    assert spec.feature_name == "Add numbers"

    with pytest.raises(ValidationError):
        CodeArtifact(
            implementation_code="print('hello')",
            test_code="",
            iteration=5
        )


def test_immediate_convergence(monkeypatch):
    spec = SpecArtifact(
        feature_name="Test",
        requirements=["Test requirement"],
        test_cases=["Test case"],
        interfaces=["test()"]
    )

    code = CodeArtifact(
        implementation_code="print('hello')",
        test_code="",
        iteration=1
    )

    qa = QAReport(
        tests_passed=1,
        total_tests=1,
        status="PASSED"
    )

    monkeypatch.setattr(
        orchestrator, "create_spec", lambda request: spec
    )
    monkeypatch.setattr(
        orchestrator, "create_code", lambda *args, **kwargs: code
    )
    monkeypatch.setattr(
        orchestrator, "review_code", lambda code: qa
    )

    result = orchestrator.run_squad("Test request")

    assert result["qa"].status == "PASSED"
    assert len(result["history"]) == 1


def test_maximum_four_cycles(monkeypatch):
    spec = SpecArtifact(
        feature_name="Test",
        requirements=["Test requirement"],
        test_cases=["Test case"],
        interfaces=["test()"]
    )

    code = CodeArtifact(
        implementation_code="print('hello')",
        test_code="",
        iteration=1
    )

    qa = QAReport(
        tests_passed=0,
        total_tests=1,
        failed_tests=["Test failed"],
        review_feedback="Please fix the code",
        status="NEEDS_REVISION"
    )

    monkeypatch.setattr(
        orchestrator, "create_spec", lambda request: spec
    )
    monkeypatch.setattr(
        orchestrator, "create_code", lambda *args, **kwargs: code
    )
    monkeypatch.setattr(
        orchestrator, "review_code", lambda code: qa
    )

    result = orchestrator.run_squad("Test request")

    assert len(result["history"]) == 4
    assert result["qa"].status == "MAX_CYCLES_EXCEEDED"


from src.schemas import CodeArtifact, QAReport
from src.sandbox import run_tests


def review_code(code: CodeArtifact) -> QAReport:

    result = run_tests(
        code.implementation_code,
        code.test_code
    )

    output = (
        result["stdout"] + "\n" + result["stderr"]
    )

    passed = result["exit_code"] == 0

    if passed:
        status = "PASSED"
        feedback = "All tests passed."
        passed_count = 1
    elif result["timed_out"]:
        status = "NEEDS_REVISION"
        feedback = "Tests exceeded the 10-second time limit."
        passed_count = 0
    else:
        status = "NEEDS_REVISION"
        feedback = "Tests failed. Please review the error output."
        passed_count = 0

    return QAReport(
        tests_passed=passed_count,
        total_tests=1,
        failed_tests=[] if passed else [feedback],
        execution_output=output,
        review_feedback=feedback,
        status=status
    )

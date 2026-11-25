
import subprocess
import sys
import tempfile
from pathlib import Path


def run_tests(implementation_code: str, test_code: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        folder = Path(temp_dir)

        (folder / "implementation.py").write_text(
            implementation_code,
            encoding="utf-8"
        )

        (folder / "test_generated.py").write_text(
            test_code,
            encoding="utf-8"
        )

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                    "test_generated.py"
                ],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=10,
                shell=False
            )

            return {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timed_out": False
            }

        except subprocess.TimeoutExpired as error:
            return {
                "exit_code": -1,
                "stdout": error.stdout or "",
                "stderr": error.stderr or "Test timed out",
                "timed_out": True
            }

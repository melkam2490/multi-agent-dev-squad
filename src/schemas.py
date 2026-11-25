
from typing import Literal
from pydantic import BaseModel, Field


class SpecArtifact(BaseModel):
    feature_name: str
    requirements: list[str]
    test_cases: list[str]
    interfaces: list[str]


class CodeArtifact(BaseModel):
    implementation_code: str
    test_code: str
    iteration: int = Field(ge=1, le=4)


class QAReport(BaseModel):
    tests_passed: int = 0
    total_tests: int = 0
    failed_tests: list[str] = Field(default_factory=list)
    execution_output: str = ""
    review_feedback: str = ""
    status: Literal[
        "PASSED",
        "NEEDS_REVISION",
        "MAX_CYCLES_EXCEEDED"
    ]

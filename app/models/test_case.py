from pydantic import BaseModel, Field
from typing import List


class TestCase(BaseModel):
    test_case_id: str
    requirement_id: str
    title: str
    preconditions: List[str] = Field(default_factory=list)
    test_steps: List[str]
    test_data: List[str] = Field(default_factory=list)
    expected_result: str
    priority: str
    severity: str
    test_type: str
    positive_negative: str
    automation_candidate: bool


class TestCaseList(BaseModel):
    test_cases: List[TestCase]
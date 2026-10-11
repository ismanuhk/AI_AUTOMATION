import json
from langchain_ollama import ChatOllama
from app.models.test_case import TestCase

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    format="json"
)


def generate_test_cases(user_story: str) -> list[TestCase]:

    prompt = f"""
You are a senior QA engineer.

Analyze this login requirement and generate EXACTLY 8 distinct test cases.

REQUIREMENT:
{user_story}

Generate exactly these 8 scenarios:

1. TC001: Login with valid credentials
2. TC002: Login with invalid email
3. TC003: Login with invalid password
4. TC004: Login with both fields empty
5. TC005: Login with empty email
6. TC006: Login with empty password
7. TC007: Login with invalid email format
8. TC008: Login with whitespace-only fields

Use these application rules:

- Valid email: user@example.com
- Valid password: Test@123
- Unregistered email: wrong@example.com
- Invalid password: InvalidPassword
- Invalid email format: manu@
- Both fields empty: Email and password are required
- Empty email: Email is required
- Empty password: Password is required
- Invalid email: Invalid email
- Invalid password: Invalid password
- Invalid email format: Invalid email format
- Whitespace-only fields: Email is required

Return JSON with this exact structure:

{{
  "test_cases": [
    {{
      "test_case_id": "TC001",
      "requirement_id": "REQ001",
      "title": "Login with valid credentials",
      "preconditions": ["Login page is available"],
      "test_steps": ["Open the login page"],
      "test_data": ["Email: user@example.com", "Password: Test@123"],
      "expected_result": "Dashboard heading is visible",
      "priority": "High",
      "severity": "High",
      "test_type": "Functional",
      "positive_negative": "Positive",
      "automation_candidate": true
    }}
  ]
}}

The example shows one item only. Your actual response MUST contain all 8 test cases.

Rules:
- Use IDs TC001 through TC008 exactly once.
- Use requirement ID REQ001.
- Give every test case a unique title.
- Every test case must have non-empty test_steps and test_data lists.
- Keep each test case focused on its assigned scenario.
- Use priority High, Medium, or Low.
- Use severity Critical, High, Medium, or Low.
- Use test types Functional, Validation, Boundary, Security, Session, UI, or Regression.
- Use Positive or Negative for positive_negative.
- Set automation_candidate to true.
- Return valid JSON only.
"""

    response = llm.invoke(prompt)
    data = json.loads(response.content)

    if "test_cases" not in data:
        raise ValueError("AI response is missing test_cases.")

    items = data["test_cases"]

    if not isinstance(items, list) or len(items) != 8:
        raise ValueError(
            f"Expected exactly 8 test cases, received {len(items) if isinstance(items, list) else 'invalid data'}."
        )

    test_cases = [
        TestCase.model_validate(item)
        for item in items
    ]

    expected_ids = {f"TC{i:03d}" for i in range(1, 9)}
    actual_ids = {case.test_case_id for case in test_cases}

    if actual_ids != expected_ids:
        raise ValueError(
            f"Unexpected test case IDs. Expected {sorted(expected_ids)}, received {sorted(actual_ids)}."
        )

    return test_cases

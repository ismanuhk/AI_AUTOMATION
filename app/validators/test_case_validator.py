from app.models.test_case import TestCase

VALID_PRIORITIES = {"High", "Medium", "Low"}

VALID_SEVERITIES = {
    "Critical", "High", "Medium", "Low"
}

VALID_TEST_TYPES = {
    "Functional",
    "Validation",
    "Boundary",
    "Security",
    "Session",
    "UI",
    "Regression"
}

VALID_POSITIVE_NEGATIVE = {
    "Positive", "Negative"
}


def validate_test_cases(
    test_cases: list[TestCase]
) -> list[str]:

    errors = []
    test_case_ids = set()
    titles = set()

    for test_case in test_cases:
        case_id = test_case.test_case_id
        title = test_case.title.strip()

        # Check duplicate IDs
        if case_id in test_case_ids:
            errors.append(
                f"{case_id}: Duplicate test case ID"
            )
        test_case_ids.add(case_id)

        # Check duplicate titles
        normalized_title = title.lower()

        if normalized_title in titles:
            errors.append(
                f"{case_id}: Duplicate test case title"
            )
        titles.add(normalized_title)

        # Check required fields
        if not title:
            errors.append(
                f"{case_id}: Title is empty"
            )

        if not test_case.requirement_id.strip():
            errors.append(
                f"{case_id}: Requirement ID is empty"
            )

        if not test_case.test_steps:
            errors.append(
                f"{case_id}: Test steps are empty"
            )
        elif any(
            not step.strip()
            for step in test_case.test_steps
        ):
            errors.append(
                f"{case_id}: A test step is empty"
            )

        if not test_case.expected_result.strip():
            errors.append(
                f"{case_id}: Expected result is empty"
            )

        if not test_case.test_data:
            errors.append(
                f"{case_id}: Test data is empty"
            )
        elif any(
            not value.strip()
            for value in test_case.test_data
        ):
            errors.append(
                f"{case_id}: A test data entry is empty"
            )

        # Check classification values
        if test_case.priority not in VALID_PRIORITIES:
            errors.append(
                f"{case_id}: Invalid priority"
            )

        if test_case.severity not in VALID_SEVERITIES:
            errors.append(
                f"{case_id}: Invalid severity"
            )

        if test_case.test_type not in VALID_TEST_TYPES:
            errors.append(
                f"{case_id}: Invalid test type"
            )

        if (
            test_case.positive_negative
            not in VALID_POSITIVE_NEGATIVE
        ):
            errors.append(
                f"{case_id}: Invalid Positive/Negative value"
            )

        if not isinstance(
            test_case.automation_candidate, bool
        ):
            errors.append(
                f"{case_id}: Automation candidate must be boolean"
            )

    return errors

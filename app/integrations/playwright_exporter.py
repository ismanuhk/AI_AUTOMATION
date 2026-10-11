import ast
import os


def validate_python_code(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
        return True, "Python syntax is valid"

    except SyntaxError as error:
        return False, f"Syntax error: {error}"


def validate_playwright_rules(code: str) -> list[str]:
    errors = []

    if "sync_playwright()" in code:
        errors.append(
            "Do not create a custom sync_playwright browser"
        )

    if "time.sleep(" in code:
        errors.append(
            "Do not use time.sleep()"
        )

    if "selenium" in code.lower():
        errors.append(
            "Selenium is not allowed"
        )

    if "expect(" not in code:
        errors.append(
            "Test must contain an expect() assertion"
        )

    if "page: Page" not in code:
        errors.append(
            "Test must use page: Page fixture"
        )

    if "def test_" not in code:
        errors.append(
            "Test function must start with test_"
        )

    return errors


def save_playwright_test(
    test_case_id: str,
    code: str,
    output_directory: str = "output/playwright_tests"
) -> str:

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    is_valid, message = validate_python_code(code)

    if not is_valid:
        raise ValueError(
            f"{test_case_id}: {message}"
        )

    rule_errors = validate_playwright_rules(code)

    if rule_errors:
        raise ValueError(
            f"{test_case_id}: Playwright validation failed: "
            + "; ".join(rule_errors)
        )

    file_path = os.path.join(
        output_directory,
        f"test_{test_case_id}.py"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(code)

    return file_path

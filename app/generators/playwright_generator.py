import re
from app.models.test_case import TestCase


def generate_playwright_test(test_case: TestCase) -> str:
    title = test_case.title.lower()

    function_name = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        title
    ).strip("_")

    function_name = (
        f"test_{test_case.test_case_id.lower()}_{function_name}"
    )

    if "whitespace" in title:
        actions = """
    page.get_by_label("Email").fill("   ")
    page.get_by_label("Password").fill("   ")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Email is required")
"""

    elif "both fields empty" in title or "empty fields" in title:
        actions = """
    page.get_by_label("Email").fill("")
    page.get_by_label("Password").fill("")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text(
        "Email and password are required"
    )
"""

    elif "empty email" in title:
        actions = """
    page.get_by_label("Email").fill("")
    page.get_by_label("Password").fill("Test@123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Email is required")
"""

    elif "empty password" in title:
        actions = """
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Password is required")
"""

    elif "invalid email format" in title or "malformed email" in title:
        actions = """
    page.get_by_label("Email").fill("manu@")
    page.get_by_label("Password").fill("Test@123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Invalid email format")
"""

    elif "invalid email" in title:
        actions = """
    page.get_by_label("Email").fill("wrong@example.com")
    page.get_by_label("Password").fill("Test@123")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Invalid email")
"""

    elif "invalid password" in title:
        actions = """
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("InvalidPassword")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#error")).to_have_text("Invalid password")
"""

    elif "valid credentials" in title:
        actions = """
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("Test@123")
    page.get_by_role("button", name="Login").click()
    expect(
        page.get_by_role("heading", name="Dashboard")
    ).to_be_visible()
"""

    else:
        raise ValueError(
            f"No Playwright template available for: {test_case.title}"
        )

    code = f'''from playwright.sync_api import Page, expect


def {function_name}(page: Page):
    page.goto("http://127.0.0.1:8000/login.html")
{actions}
'''

    compile(code, f"{test_case.test_case_id}.py", "exec")

    return code

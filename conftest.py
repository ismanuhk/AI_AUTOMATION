import os
import pytest
from pytest_html import extras


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "executable_path": r"C:\Users\Manu H K\AppData\Local\ms-playwright\chromium-1194\chrome-win\chrome.exe",
        "headless": True,
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")

    if page is None:
        return

    screenshot_dir = "output/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    screenshot_path = os.path.abspath(
        os.path.join(screenshot_dir, f"{item.name}.png")
    )

    try:
        page.screenshot(path=screenshot_path, full_page=True)

        report.extra = getattr(report, "extra", [])
        report.extra.append(
            extras.image(
                screenshot_path,
                name="Failure Screenshot"
            )
        )

        print(f"\nScreenshot saved: {screenshot_path}")

    except Exception as error:
        print(f"\nCould not save screenshot: {error}")

import os
import subprocess
import sys
import time
import urllib.request


def wait_for_server(url: str, timeout: int = 10) -> bool:
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)

    return False


def run_playwright_tests(
    test_directory: str = "output/playwright_tests"
) -> tuple[bool, str]:

    os.makedirs("output/reports", exist_ok=True)

    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            "8000",
            "--directory",
            "demo_app",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not wait_for_server(
            "http://127.0.0.1:8000/login.html"
        ):
            return False, "Demo application failed to start."

        report_file = "output/reports/test_report.html"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                test_directory,
                "-v",
                "--html",
                report_file,
                "--self-contained-html",
            ],
            capture_output=True,
            text=True,
        )

        output = result.stdout + "\n" + result.stderr

        return result.returncode == 0, output

    finally:
        server.terminate()

        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()
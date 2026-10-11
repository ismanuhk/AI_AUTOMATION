import re

from app.runners.playwright_runner import run_playwright_tests
from app.agents.failure_analyzer import FailureAnalyzer


def extract_test_counts(output: str):
    passed = 0
    failed = 0

    match = re.search(
        r"(\d+)\s+failed(?:,\s*)?(\d+)\s+passed|(\d+)\s+passed(?:,\s*)?(\d+)\s+failed",
        output
    )

    if match:
        groups = match.groups()

        if groups[0] is not None:
            failed = int(groups[0])
            passed = int(groups[1])
        else:
            passed = int(groups[2])
            failed = int(groups[3])
    else:
        passed_match = re.search(r"(\d+)\s+passed", output)
        failed_match = re.search(r"(\d+)\s+failed", output)

        if passed_match:
            passed = int(passed_match.group(1))

        if failed_match:
            failed = int(failed_match.group(1))

    return passed + failed, passed, failed


def analyze_failures(output: str):
    failure_pattern = re.compile(
        r"_{3,}\s*(.*?)\s*_{3,}\s*\n(.*?)(?=\n_{3,}|\n=+ short test summary info =+|\Z)",
        re.DOTALL
    )

    failures = failure_pattern.findall(output)

    if not failures:
        print("\nNo detailed failure blocks were detected in the Pytest output.")
        print("Check the HTML report for complete failure details.")
        return

    try:
        analyzer = FailureAnalyzer()
    except Exception as error:
        print(f"\nCould not initialize AI analyzer: {error}")
        return

    for test_name, error_message in failures:
        test_name = test_name.strip()
        error_message = error_message.strip()

        print("\n" + "=" * 60)
        print(f"AI ANALYSIS: {test_name}")
        print("=" * 60)

        try:
            analysis = analyzer.analyze_failure(test_name, error_message)
            print(analysis)

            report_path = analyzer.save_analysis(test_name, analysis)
            print(f"\nAI analysis saved to: {report_path}")

        except Exception as error:
            print(f"AI analysis failed: {error}")


def main():
    print("=" * 60)
    print("RUNNING PLAYWRIGHT TESTS")
    print("=" * 60)

    passed_status, output = run_playwright_tests()

    print("\nPYTEST RESULT")
    print("=" * 60)
    print("PLAYWRIGHT TESTS PASSED" if passed_status else "PLAYWRIGHT TESTS FAILED")

    total, passed, failed = extract_test_counts(output)

    print("\nTEST EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total Tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    pass_rate = (passed / total * 100) if total else 0
    print(f"Pass Rate   : {pass_rate:.0f}%")
    print("Report      : output/reports/test_report.html")
    print("=" * 60)

    if failed > 0:
        print("\nStarting AI failure analysis...")
        analyze_failures(output)

    print("\nPYTEST OUTPUT")
    print("=" * 60)
    print(output)


if __name__ == "__main__":
    main()

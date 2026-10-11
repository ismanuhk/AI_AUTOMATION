from app.parsers.text_parser import read_text_file
from app.generators.test_case_generator import generate_test_cases
from app.validators.test_case_validator import validate_test_cases
from app.integrations.excel_exporter import export_to_excel
from app.integrations.test_management import save_test_cases
from app.generators.playwright_generator import generate_playwright_test
from app.integrations.playwright_exporter import save_playwright_test


def main():

    file_path = "test_data/login_requirement.txt"

    print("=" * 60)
    print("AI TEST CASE GENERATOR")
    print("=" * 60)

    print("\nReading requirement file...")

    user_story = read_text_file(file_path)

    print("Requirement loaded successfully.")

    print("\nGenerating test cases...")

    test_cases = generate_test_cases(user_story)

    print(f"Generated {len(test_cases)} test cases.")

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    errors = validate_test_cases(test_cases)

    print("\nVALIDATION RESULT")
    print("=" * 60)

    if errors:

        print("Validation FAILED")

        for error in errors:
            print(f"ERROR: {error}")

        return

    else:
        print("Validation PASSED")

    # --------------------------------------------------
    # SAVE JSON TEST CASES
    # --------------------------------------------------

    print("\nTEST MANAGEMENT")
    print("=" * 60)

    save_test_cases(
        test_cases,
        "output/test_cases.json"
    )

    # --------------------------------------------------
    # EXPORT EXCEL
    # --------------------------------------------------

    print("\nEXCEL EXPORT")
    print("=" * 60)

    output_file = "output/test_cases.xlsx"

    export_to_excel(
        test_cases,
        output_file
    )

    # --------------------------------------------------
    # DISPLAY TEST CASES
    # --------------------------------------------------

    print("\nGENERATED TEST CASES")
    print("=" * 60)

    for test_case in test_cases:

        print(f"\nID: {test_case.test_case_id}")

        print(
            f"Requirement: "
            f"{test_case.requirement_id}"
        )

        print(
            f"Title: "
            f"{test_case.title}"
        )

        print(
            f"Priority: "
            f"{test_case.priority}"
        )

        print(
            f"Severity: "
            f"{test_case.severity}"
        )

        print(
            f"Type: "
            f"{test_case.test_type}"
        )

        print(
            f"Positive/Negative: "
            f"{test_case.positive_negative}"
        )

        print(
            f"Automation: "
            f"{test_case.automation_candidate}"
        )

        print("\nSteps:")

        for step in test_case.test_steps:
            print(f"  - {step}")

        print("\nTest Data:")

        for data in test_case.test_data:
            print(f"  - {data}")

        print(
            f"\nExpected: "
            f"{test_case.expected_result}"
        )

    # --------------------------------------------------
    # PLAYWRIGHT GENERATION
    # --------------------------------------------------

    print("\nPLAYWRIGHT AUTOMATION")
    print("=" * 60)

    for test_case in test_cases:

        if not test_case.automation_candidate:
            print(
                f"\nSkipping "
                f"{test_case.test_case_id}"
                f" because it is not an automation candidate."
            )
            continue

        print(
            f"\nGenerating Playwright test "
            f"for {test_case.test_case_id}..."
        )

        playwright_code = generate_playwright_test(
            test_case
        )

        try:

            generated_file = save_playwright_test(
                test_case.test_case_id,
                playwright_code
            )

            print(
                f"Saved: "
                f"{generated_file}"
            )

        except ValueError as error:

            print(
                f"FAILED: "
                f"{error}"
            )

    # --------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)

    print(
        f"Test Cases : "
        f"{len(test_cases)}"
    )

    print(
        "JSON       : "
        "output/test_cases.json"
    )

    print(
        "Excel      : "
        "output/test_cases.xlsx"
    )

    print(
        "Playwright : "
        "output/playwright_tests/"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
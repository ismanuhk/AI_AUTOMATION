import json
import os

from app.models.test_case import TestCase


def save_test_cases(
    test_cases: list[TestCase],
    output_file: str = "output/test_cases.json"
):
    output_directory = os.path.dirname(output_file)

    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    data = {
        "total_test_cases": len(test_cases),
        "test_cases": [
            test_case.model_dump()
            for test_case in test_cases
        ]
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Test cases saved: {output_file}")

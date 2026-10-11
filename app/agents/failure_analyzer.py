import os
from datetime import datetime
from langchain_ollama import ChatOllama


class FailureAnalyzer:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0
        )

    def analyze_failure(self, test_name, error_message):
        prompt = f"""
You are a Senior QA Automation Engineer.

Analyze this Playwright test failure using only the available evidence.

TEST NAME:
{test_name}

ERROR AND TRACEBACK:
{error_message}

Rules:
- Do not invent missing information.
- Distinguish intentional failures from application defects.
- Do not recommend changing assertions merely to make tests pass.
- If evidence is insufficient, explain what needs investigation.

Return these sections:
1. FAILURE SUMMARY
2. ERROR CATEGORY
3. EVIDENCE
4. POSSIBLE ROOT CAUSE
5. RECOMMENDED FIX
6. PREVENTION
"""

        response = self.llm.invoke(prompt)
        return response.content

    def save_analysis(self, test_name, analysis):
        report_path = os.path.join(
            "output",
            "reports",
            "ai_failure_analysis.txt"
        )

        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, "a", encoding="utf-8") as report:
            report.write("\n" + "=" * 70 + "\n")
            report.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
            report.write(f"Test: {test_name}\n")
            report.write("=" * 70 + "\n\n")
            report.write(analysis)
            report.write("\n")

        return report_path


if __name__ == "__main__":
    analyzer = FailureAnalyzer()

    test_name = "test_intentional_failure"
    error_message = (
        "AssertionError: Intentional failure to test AI analysis\n"
        "assert False"
    )

    analysis = analyzer.analyze_failure(test_name, error_message)

    print("\nAI FAILURE ANALYSIS")
    print("=" * 50)
    print(analysis)

    path = analyzer.save_analysis(test_name, analysis)
    print(f"\nAnalysis saved to: {path}")

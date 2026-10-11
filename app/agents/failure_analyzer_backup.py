from langchain_ollama import ChatOllama


class FailureAnalyzer:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0
        )

    def analyze_failure(self, test_name, error_message):
        prompt = f"""
You are an experienced Senior QA Automation Engineer.

Analyze the following Playwright test failure carefully.

TEST NAME:
{test_name}

ACTUAL ERROR AND TRACEBACK:
{error_message}

RULES:
1. Use only evidence available in the test name and error.
2. Never assume the failure is an application bug without evidence.
3. Distinguish intentional assertion failures from unexpected failures.
4. For AssertionError, explain what the expected and actual results indicate.
5. For locator errors, identify the likely locator or element problem.
6. For timeout errors, explain what timed out and possible reasons.
7. For connection errors, consider server availability and network issues.
8. Do not recommend changing a failing assertion to True just to pass a test.
9. If the evidence is insufficient, explicitly say what needs checking.
10. Give a practical fix, but do not claim it is confirmed without verification.

Return these sections:

1. FAILURE SUMMARY
Explain what failed.

2. ERROR CATEGORY
Classify the failure as Assertion, Locator, Timeout, Application,
Environment, Test Script, or Unknown.

3. EVIDENCE
Quote the relevant part of the error and explain what it proves.

4. POSSIBLE ROOT CAUSE
Give the most likely cause and distinguish it from speculation.

5. RECOMMENDED FIX
Give specific debugging steps or a code correction when justified.
Do not invent application behavior or source code.

6. PREVENTION
Explain how to reduce similar failures in future tests.
"""

        response = self.llm.invoke(prompt)
        return response.content


if __name__ == "__main__":
    analyzer = FailureAnalyzer()

    result = analyzer.analyze_failure(
        test_name="test_intentional_failure",
        error_message=(
            "AssertionError: Intentional failure to test AI analysis\n"
            "assert False"
        )
    )

    print("\nAI FAILURE ANALYSIS")
    print("=" * 50)
    print(result)

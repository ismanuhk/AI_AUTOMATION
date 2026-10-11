from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def ask_ai(user_story: str) -> str:
    prompt = f"""
You are a senior QA automation engineer.

Analyze the following user story:

{user_story}

Generate QA test scenarios covering:

1. Functional testing
2. Positive testing
3. Negative testing
4. Boundary testing
5. Validation testing
6. Security testing

Give clear test scenarios with expected results.
"""

    response = llm.invoke(prompt)

    return response.content
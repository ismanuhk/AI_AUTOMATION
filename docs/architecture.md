# AI Test Case Generator Architecture

```mermaid
flowchart TD
    A[User Requirement] --> B[Text Parser]
    B --> C[Ollama - Llama 3.2]
    C --> D[AI Test Case Generator]
    D --> E[Pydantic Validation]

    E --> F[JSON Export]
    E --> G[Excel Export]
    E --> H[Playwright Script Generator]

    H --> I[Pytest Test Runner]
    I --> J[Chromium Browser]
    J --> K[HTML Test Report]

    I --> L{Tests Failed?}
    L -- Yes --> M[AI Failure Analyzer]
    M --> N[Root Cause and Fix Suggestions]
    L -- No --> O[All Tests Passed]
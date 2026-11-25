

\# AI Prompt Audit Log



\## 1. Initial Prompt



Build a three-agent collaborative software development squad.



The agents are:

\- Product Specification Agent

\- Coder Agent

\- Reviewer / QA Agent



The agents should work together to create, test, review, and improve Python code.



\## 2. Problems Identified



\### Problem 1: Unsafe Shell Execution

Using shell=True can create security risks when executing generated code.



Correction:

\- Used subprocess.run()

\- Set shell=False

\- Added a 10-second timeout.



\### Problem 2: Too Much Context

Sending the complete conversation history to every agent can create unnecessary context and increase token usage.



Correction:

\- Send only the specification and latest QA feedback to the Coder Agent.



\### Problem 3: Incorrect Test Results

An AI agent might claim that code passes without actually running the tests.



Correction:

\- The Reviewer Agent executes pytest.

\- The test exit code determines whether tests passed.



\## 3. Final Improvements



\- Added Pydantic schemas for structured outputs.

\- Added temporary-directory test execution.

\- Added a maximum of four development cycles.

\- Added QA feedback to improve generated code.

\- Added six automated project tests.



\## 4. Final Result



The project successfully completed six automated tests.



Status: PASSED.




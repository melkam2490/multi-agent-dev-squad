
from src.agents.spec_agent import create_spec
from src.agents.coder_agent import create_code
from src.agents.reviewer_agent import review_code
from src.schemas import QAReport


def run_squad(user_request: str, max_cycles: int = 4):

    # Agent 1: Create the product specification
    spec = create_spec(user_request)

    feedback = ""
    history = []
    code = None
    qa = None

    # Run the coder and reviewer for up to 4 cycles
    for cycle in range(1, max_cycles + 1):

        # Agent 2: Write code
        code = create_code(
            spec,
            iteration=cycle,
            feedback=feedback
        )

        # Agent 3: Test and review the code
        qa = review_code(code)

        history.append({
            "iteration": cycle,
            "status": qa.status,
            "feedback": qa.review_feedback
        })

        # Stop if all tests pass
        if qa.status == "PASSED":
            break

        feedback = qa.execution_output + "\n" + qa.review_feedback

    # Stop after the maximum number of cycles
    if qa.status != "PASSED":
        qa.status = "MAX_CYCLES_EXCEEDED"

    return {
        "spec": spec,
        "code": code,
        "qa": qa,
        "history": history
    }


import json
from openai import OpenAI
from src.schemas import SpecArtifact, CodeArtifact


def create_code(
    spec: SpecArtifact,
    iteration: int = 1,
    feedback: str = ""
) -> CodeArtifact:

    client = OpenAI()

    prompt = f"""
    Build Python code based on this specification:

    {spec.model_dump_json()}

    Previous QA feedback:
    {feedback}

    Return JSON with:
    implementation_code
    test_code

    The implementation must be in implementation.py.
    Tests must import the implementation.
    Write pytest tests.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a Python Coder Agent. Return valid JSON only."
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    data["iteration"] = iteration

    return CodeArtifact(**data)


import json
from openai import OpenAI
from src.schemas import SpecArtifact


def create_spec(user_request: str) -> SpecArtifact:
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are a Product Specification Agent.
                Read the user's request and create:
                - feature_name
                - requirements (list of strings)
                - test_cases (list of strings)
                - interfaces (list of strings)

                Return valid JSON only.
                """
            },
            {"role": "user", "content": user_request}
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return SpecArtifact(**data)

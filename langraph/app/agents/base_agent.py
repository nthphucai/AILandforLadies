import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

is_docker_desktop_enabled = os.getenv("docker_desktop_enabled", "False")

if is_docker_desktop_enabled:
    # Use Docker Desktop's host IP for ollama API endpoint
    ollama_api_endpoint = "http://host.docker.internal:11434/v1"
else:
    # Use localhost for ollama API endpoint
    ollama_api_endpoint = "http://localhost:11434/v1"

ollama_api_endpoint = "http://localhost:11434/v1"

client = OpenAI(
    base_url=ollama_api_endpoint, api_key=os.getenv("ollama_api_key", "ollama")
)

model = os.getenv("ollama_model")

class BaseAgent:
    """Base class for all agents in the Langraph workflow."""

    def __init__(self, name: str):
        self.name = name

    def parse_response(self, system_prompt, content, response_format):

        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": str(content)},
            ],
            response_format=response_format,
            temperature=0.1,
            top_p=0.85,
            presence_penalty=0.0,
            seed=42,
        )
        response = completion.choices[0].message.parsed
        return response

    def create_response(self, system_prompt, content):
        """Create a response using the OpenAI API."""
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": str(content)},
            ],
        )
        return completion.choices[0].message.content

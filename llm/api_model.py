from .base import BaseLLM

class APIModel(BaseLLM):
    def __init__(self, client):
        self.client = client

    def generate(self, prompt: str) -> str:
        response = self.client.call(prompt)
        return response

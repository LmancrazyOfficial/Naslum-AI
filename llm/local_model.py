import requests

class LocalLLM:

    def __init__(self, endpoint="http://localhost:11434/api/generate"):
        self.endpoint = endpoint

    def generate(self, prompt: str):
        response = requests.post(self.endpoint, json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })

        return response.json()["response"]

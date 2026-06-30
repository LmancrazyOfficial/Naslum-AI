from .base import BaseLLM

class LocalModel(BaseLLM):
    def generate(self, prompt: str) -> str:
        return f"""
You are an expert software engineer.

Task:
{prompt}

Return:
- architecture
- file structure
- code
"""

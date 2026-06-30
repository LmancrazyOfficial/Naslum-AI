from llm.base import BaseLLM

class LocalModel(BaseLLM):
    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "No local model is connected yet. "
            "This will be implemented in a later version."
        )

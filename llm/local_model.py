from llm.base import BaseLLM


class LocalModel(BaseLLM):

    def __init__(self, backend=None):
        """
        backend can later be:
        - OpenAI client
        - Ollama
        - LM Studio
        - custom local model
        """
        self.backend = backend

    def generate(self, prompt: str) -> str:

        # -----------------------------
        # TEMP FALLBACK (no backend)
        # -----------------------------
        if self.backend is None:
            return self._mock_response(prompt)

        # -----------------------------
        # REAL BACKEND CALL (future-ready)
        # -----------------------------
        return self.backend.generate(prompt)

    def _mock_response(self, prompt: str) -> str:
        """
        Safe placeholder so system still runs.
        This will NOT be used in final version.
        """

        # Very minimal structured fallback
        return """
{
  "files": {
    "main.py": "print('AI Factory running')"
  },
  "next_task": "test"
}
"""

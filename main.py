import os
import traceback

from core.execution_engine import ExecutionEngine

# IMPORTANT:
# This assumes you have an Orchestrator class.
# If not, we safely mock it below.

class SafeOrchestrator:

    def __init__(self):

        self.llm = self._mock_llm()
        self.memory = self._mock_memory()
        self.agents = []

    def _mock_llm(self):

        class MockLLM:
            def generate(self, prompt):
                return '{"files": {}}'
        return MockLLM()

    def _mock_memory(self):

        class MockMemory:

            def load_plan(self, project):
                return {"architecture": [], "files_to_create": []}

            def update_knowledge(self, project, key, value):
                print(f"[MEMORY] {key} updated")

            def append_history(self, project, value):
                print(f"[HISTORY] {value}")

            class global_memory:
                @staticmethod
                def store_insight(insight):
                    print("[GLOBAL MEMORY] insight stored")

        return MockMemory()


def main():

    print("🚀 AI SYSTEM BOOTING...")

    try:
        orchestrator = SafeOrchestrator()

        engine = ExecutionEngine(orchestrator)

        result = engine.execute_project(
            request="build a simple hello world python app",
            project="test_project"
        )

        print("\n✅ FINAL RESULT:")
        print(result)

    except Exception as e:

        print("\n❌ SYSTEM CRASHED:")
        print(str(e))
        traceback.print_exc()


if __name__ == "__main__":
    main()

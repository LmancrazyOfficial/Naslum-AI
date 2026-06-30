import os

from agents.base_agent import BaseAgent
from core.task import Task
from core.sandbox import Sandbox


class TesterAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)
        self.sandbox = Sandbox()

    def can_handle(self, task: Task):
        return task.task_type == "test"

    def execute(self, task: Task):

        project = task.data.get("project")

        # Try running main entry point
        result = self.sandbox.run_python_file("main.py")

        test_result = {
            "success": result["success"],
            "output": result["output"],
            "error": result["error"]
        }

        # Store real test result in memory
        self.memory.update_knowledge(
            project,
            "last_test",
            test_result
        )

        self.memory.append_history(
            project,
            {
                "event": "test_run",
                "success": result["success"]
            }
        )

        return test_result

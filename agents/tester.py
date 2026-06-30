from agents.base_agent import BaseAgent
from core.task import Task
import subprocess
import os


class TesterAgent(BaseAgent):
    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)

    def can_handle(self, task: Task):
        return task.task_type == "test"

    def execute(self, task: Task):

        command = task.data.get("command")

        if command is None:
            command = "python main.py"

        result = self.tools.run_command(command)

        success = result["returncode"] == 0

        report = {
            "success": success,
            "stdout": result["stdout"],
            "stderr": result["stderr"]
        }

        self.memory.add_knowledge(
            "last_test",
            report
        )

        return report

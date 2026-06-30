import json
import os

from agents.base_agent import BaseAgent
from core.task import Task


class CoderAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)

    def can_handle(self, task: Task):
        return task.task_type == "code"

    def execute(self, task: Task):

        plan = self.memory.get_knowledge(
            "default",
            "last_plan"
        )

        prompt = f"""
You are a senior software engineer.

You must generate a COMPLETE working multi-file project.

ARCHITECTURE PLAN:
{plan}

Return ONLY valid JSON in this format:

{{
  "files": {{
    "main.py": "print('hello')",
    "utils/helper.py": "def help(): pass"
  }},
  "next_task": "test"
}}
"""

        response = self.llm.generate(prompt)

        try:
            data = json.loads(response)
        except Exception:
            return {
                "error": "Invalid JSON from LLM",
                "raw": response
            }

        files = data.get("files", {})

        # Write files into workspace
        for path, content in files.items():

            full_path = os.path.join("workspace", path)

            os.makedirs(
                os.path.dirname(full_path),
                exist_ok=True
            )

            self.tools.write_file(path, content)

        # Create next task (self-driving behavior)
        next_task = data.get("next_task")

        if next_task:
            self.memory.update_knowledge(
                "default",
                "next_task",
                next_task
            )

        return {
            "files_created": list(files.keys()),
            "next_task": next_task
        }

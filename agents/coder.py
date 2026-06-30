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

        fix_mode = task.data.get("fix_mode", False)
        errors = task.data.get("errors", None)

        if fix_mode:
            prompt = f"""
You are an expert debugging engineer.

You are fixing an existing broken project.

ARCHITECTURE PLAN:
{plan}

ERRORS FROM TEST RUN:
{json.dumps(errors, indent=2)}

TASK:
- Identify the root cause
- Fix ONLY the broken parts
- Do NOT rewrite the entire project unnecessarily

Return ONLY valid JSON:

{{
  "files": {{
    "path/to/file.py": "fixed code"
  }},
  "next_task": "test"
}}
"""
        else:
            prompt = f"""
You are a senior software engineer.

Generate a COMPLETE working multi-file project.

ARCHITECTURE PLAN:
{plan}

Return ONLY valid JSON:

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

        # Write only changed files
        for path, content in files.items():

            full_path = os.path.join("workspace", path)

            os.makedirs(
                os.path.dirname(full_path),
                exist_ok=True
            )

            self.tools.write_file(path, content)

        # Store next step
        next_task = data.get("next_task")

        if next_task:
            self.memory.update_knowledge(
                "default",
                "next_task",
                next_task
            )

        return {
            "fix_mode": fix_mode,
            "files_updated": list(files.keys()),
            "next_task": next_task
        }

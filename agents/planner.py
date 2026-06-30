from agents.base_agent import BaseAgent
from core.task import Task


class PlannerAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)

    def can_handle(self, task: Task):
        return task.task_type == "plan"

    def execute(self, task: Task):

        request = task.data.get("request", "")

        prompt = f"""
You are a senior software architect.

Break this request into a structured software development plan.

USER REQUEST:
{request}

Return ONLY valid JSON in this format:

{{
  "project_name": "string",
  "overview": "string",
  "architecture": [
    "component 1",
    "component 2"
  ],
  "task_flow": [
    "plan",
    "code",
    "test"
  ],
  "files_to_create": [
    "file1.py",
    "file2.py"
  ],
  "notes": [
    "important constraints"
  ]
}}
"""

        response = self.llm.generate(prompt)

        # Store in memory for later agents
        self.memory.update_knowledge(
            "default",
            "last_plan",
            response
        )

        return response

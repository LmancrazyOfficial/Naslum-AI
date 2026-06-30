from agents.base_agent import BaseAgent
from core.task import Task


class PlannerAgent(BaseAgent):
    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)

    def can_handle(self, task: Task):
        return task.task_type == "plan"

    def execute(self, task: Task):

        request = task.data["request"]

        prompt = f"""
You are an expert software architect.

Break this request into a development plan.

User Request:
{request}

Return ONLY valid JSON.

Format:

{{
    "project_name": "",
    "description": "",
    "steps": [],
    "files": [],
    "languages": [],
    "dependencies": []
}}
"""

        response = self.llm.generate(prompt)

        # Save the latest generated plan
        self.memory.add_knowledge(
            "last_plan",
            response
        )

        return response

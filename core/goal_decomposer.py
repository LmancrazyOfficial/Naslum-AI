import json


class GoalDecomposer:

    def __init__(self, llm):
        self.llm = llm

    def decompose(self, goal: str):

        prompt = f"""
You are an autonomous software planning system.

Break this HIGH-LEVEL GOAL into executable sub-projects.

GOAL:
{goal}

Rules:
- Decompose into logical modules
- Each module should be independently implementable
- Include dependencies between modules
- Keep it realistic for software engineering

Return ONLY valid JSON:

{{
  "project_name": "string",
  "modules": [
    {{
      "name": "module name",
      "description": "what it does",
      "dependencies": ["other modules"],
      "tasks": [
        "task 1",
        "task 2"
      ]
    }}
  ]
}}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except Exception:
            return {
                "error": "Invalid decomposition output",
                "raw": response
            }

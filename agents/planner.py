import json

from agents.base_agent import BaseAgent
from core.task import Task


class PlannerAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)

    def can_handle(self, task: Task):
        return task.task_type == "plan"

    def execute(self, task: Task):

        project = task.data.get("project", "default")
        request = task.data.get("request", "")

        # -----------------------------
        # Load learning data
        # -----------------------------
        patterns = self.memory.get_patterns(project)
        history = self.memory._read_json(
            self.memory._project_path(project) + "/history.json"
        )

        prompt = f"""
You are a senior software architect that improves over time.

USER REQUEST:
{request}

PAST SUCCESSFUL PATTERNS:
{json.dumps(patterns, indent=2)}

PROJECT HISTORY:
{json.dumps(history, indent=2)}

TASK:
Create the BEST possible software architecture plan.

Rules:
- Reuse successful patterns when relevant
- Avoid repeating past mistakes
- Improve structure based on history
- Keep it practical and implementable

Return ONLY valid JSON:

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

        try:
            plan = json.loads(response)
        except Exception:
            return {
                "error": "Invalid JSON from LLM",
                "raw": response
            }

        # -----------------------------
        # Save plan + learn
        # -----------------------------
        self.memory.save_plan(project, plan)

        self.memory.append_history(
            project,
            {"event": "plan_generated"}
        )

        # Store architecture as a reusable pattern
        self.memory.store_pattern(
            project,
            {
                "architecture": plan.get("architecture"),
                "files": plan.get("files_to_create")
            }
        )

        return plan

import json
from datetime import datetime


class SelfImprover:

    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory

    def analyze_project(self, project):

        history = self.memory._read_json(
            self.memory._project_path(project) + "/history.json"
        )

        patterns = self.memory.get_patterns(project)
        global_patterns = self.memory.global_patterns()
        failures = self.memory.global_failures()

        prompt = f"""
You are an autonomous software improvement engine.

Analyze this system and generate improvements.

PROJECT HISTORY:
{json.dumps(history, indent=2)}

PROJECT PATTERNS:
{json.dumps(patterns, indent=2)}

GLOBAL PATTERNS:
{json.dumps(global_patterns, indent=2)}

GLOBAL FAILURES:
{json.dumps(failures, indent=2)}

TASK:
- Identify inefficiencies
- Detect repeated failures
- Suggest architectural improvements
- Propose new capabilities

Return ONLY valid JSON:

{{
  "insights": [
    "insight 1",
    "insight 2"
  ],
  "improvement_tasks": [
    {{
      "type": "refactor|feature|fix",
      "description": "what should be improved"
    }}
  ]
}}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except Exception:
            return {
                "error": "Invalid self-improvement output",
                "raw": response
            }

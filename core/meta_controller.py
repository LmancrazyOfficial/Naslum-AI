import json
from datetime import datetime


class MetaController:

    def __init__(self, llm, memory):

        self.llm = llm
        self.memory = memory

    def evolve_strategy(self):

        global_patterns = self.memory.global_patterns()
        global_failures = self.memory.global_failures()
        insights = self.memory.global_insights()

        prompt = f"""
You are a META-LEVEL AI CONTROLLER.

Your job is NOT to build software.

Your job is to improve HOW this AI system builds software.

You control:
- planning strategy
- coding strategy
- testing strategy
- agent coordination

DATA:

GLOBAL PATTERNS:
{json.dumps(global_patterns, indent=2)}

GLOBAL FAILURES:
{json.dumps(global_failures, indent=2)}

GLOBAL INSIGHTS:
{json.dumps(insights, indent=2)}

TASK:
- Identify systemic weaknesses
- Suggest strategy changes
- Propose agent behavior improvements
- Optimize full execution pipeline

Return ONLY valid JSON:

{{
  "strategy_updates": [
    {{
      "component": "planner|coder|tester|engine",
      "change": "what should change",
      "reason": "why"
    }}
  ],
  "new_rules": [
    "rule 1",
    "rule 2"
  ]
}}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except Exception:
            return {
                "error": "Invalid meta output",
                "raw": response
            }

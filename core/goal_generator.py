import json
from datetime import datetime


class GoalGenerator:

    def __init__(self, llm, memory):

        self.llm = llm
        self.memory = memory

    def generate_goals(self):

        global_insights = self.memory.global_insights()
        global_failures = self.memory.global_failures()
        global_patterns = self.memory.global_patterns()

        prompt = f"""
You are an AUTONOMOUS GOAL GENERATION ENGINE.

Your job:
- Analyze system behavior
- Identify missing capabilities
- Detect inefficiencies
- Propose NEW SOFTWARE PROJECTS the system should build

DATA:

INSIGHTS:
{json.dumps(global_insights, indent=2)}

FAILURES:
{json.dumps(global_failures, indent=2)}

PATTERNS:
{json.dumps(global_patterns, indent=2)}

RULES:
- Only propose meaningful software engineering goals
- Avoid duplicates
- Prefer system improvements or infrastructure upgrades
- Keep goals executable by the agent swarm

Return ONLY valid JSON:

{{
  "new_goals": [
    {{
      "priority": "low|medium|high",
      "goal": "string description",
      "reason": "why this should be built"
    }}
  ]
}}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except Exception:
            return {
                "error": "Invalid goal generation output",
                "raw": response
            }

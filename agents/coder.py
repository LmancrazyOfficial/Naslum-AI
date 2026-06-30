import os
import json

class CoderAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate_project(self, plan, workspace):

        prompt = f"""
You are a senior software architect.

Create a FULL multi-file project.

PLAN:
{plan}

Return STRICT JSON:
{{
  "files": {{
    "path/to/file": "code"
  }}
}}
"""

        output = self.llm.generate(prompt)

        data = json.loads(output)

        for path, code in data["files"].items():
            full_path = os.path.join(workspace, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w") as f:
                f.write(code)

        return data

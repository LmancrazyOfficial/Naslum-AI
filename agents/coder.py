import os
import json

class CoderAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_project(self, plan, workspace):
        prompt = f"""
You are a senior software engineer.

Based on this software plan:

{plan}

Generate a COMPLETE multi-file project.

Return ONLY valid JSON in this format:

{{
  "files": {{
    "main.py": "print('Hello')",
    "README.md": "# Project"
  }}
}}
"""

        output = self.llm.generate(prompt)

        try:
            data = json.loads(output)

            for path, code in data["files"].items():
                full_path = os.path.join(workspace, path)

                os.makedirs(os.path.dirname(full_path) or workspace, exist_ok=True)

                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(code)

            return data

        except Exception as e:
            return {
                "error": f"Failed to generate project: {e}",
                "raw_output": output
            }

    def fix_code(self, fix_prompt, workspace):
        prompt = f"""
You are an expert software debugging AI.

PROJECT PLAN:
{fix_prompt['plan']}

ERRORS:
{fix_prompt['errors']}

PROJECT ANALYSIS:
{fix_prompt['analysis']}

Fix the project.

Return ONLY valid JSON:

{{
  "files": {{
    "path/to/file.py": "corrected code"
  }}
}}
"""

        output = self.llm.generate(prompt)

        try:
            data = json.loads(output)

            for path, code in data["files"].items():
                full_path = os.path.join(workspace, path)

                os.makedirs(os.path.dirname(full_path) or workspace, exist_ok=True)

                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(code)

            return data

        except Exception as e:
            return {
                "error": f"Failed to fix project: {e}",
                "raw_output": output
            }

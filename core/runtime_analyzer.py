import json
import traceback


class RuntimeAnalyzer:

    def __init__(self, llm):
        self.llm = llm

    def analyze_error(self, error_context, code_context):

        prompt = f"""
You are a senior debugging engineer.

Your job is to find the ROOT CAUSE of runtime errors.

========================
ERROR OUTPUT
========================
{json.dumps(error_context, indent=2)}

========================
RELEVANT CODE
========================
{json.dumps(code_context, indent=2)}

TASK:
- Identify root cause (not symptoms)
- Identify exact file + line likely responsible
- Suggest minimal fix strategy
- Avoid rewriting full system unless necessary

Return ONLY valid JSON:

{{
  "root_cause": "string",
  "affected_files": ["file1", "file2"],
  "fix_strategy": "string",
  "confidence": 0.0
}}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except Exception:
            return {
                "error": "Invalid runtime analysis",
                "raw": response
            }

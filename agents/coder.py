import json
import os

from agents.base_agent import BaseAgent
from core.task import Task
from core.project_indexer import ProjectIndexer


class CoderAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)
        self.indexer = ProjectIndexer()

    def can_handle(self, task: Task):
        return task.task_type == "code"

    def execute(self, task: Task):

        project = task.data.get("project")
        fix_mode = task.data.get("mode") == "fix"
        errors = task.data.get("errors")

        # -----------------------------
        # Build project context
        # -----------------------------
        project_path = os.path.join("workspace")

        index = self.indexer.build_index(project_path)

        plan = self.memory.load_plan(project)

        # -----------------------------
        # Prompt construction
        # -----------------------------
        if fix_mode:

            prompt = f"""
You are a senior software engineer debugging a real codebase.

PROJECT PLAN:
{json.dumps(plan, indent=2)}

PROJECT STRUCTURE:
{json.dumps(index, indent=2)}

ERRORS:
{json.dumps(errors, indent=2)}

RULES:
- Do NOT rewrite everything
- Only fix affected files
- Respect existing architecture
- Keep dependencies consistent

Return ONLY valid JSON:

{{
  "files": {{
    "path/to/file.py": "fixed code"
  }},
  "next_task": "test"
}}
"""

        else:

            prompt = f"""
You are a senior software engineer.

You are building a project using this architecture:

PROJECT PLAN:
{json.dumps(plan, indent=2)}

PROJECT STRUCTURE (current state, may be empty initially):
{json.dumps(index, indent=2)}

RULES:
- Use existing structure if available
- Do not duplicate functionality
- Respect dependencies
- Split code properly across files

Return ONLY valid JSON:

{{
  "files": {{
    "main.py": "code here",
    "utils/helper.py": "code here"
  }},
  "next_task": "test"
}}
"""

        # -----------------------------
        # Generate response
        # -----------------------------
        response = self.llm.generate(prompt)

        try:
            data = json.loads(response)
        except Exception:
            return {
                "error": "Invalid JSON from LLM",
                "raw": response
            }

        files = data.get("files", {})

        # -----------------------------
        # Write files safely
        # -----------------------------
        for path, content in files.items():

            full_path = os.path.join("workspace", path)

            os.makedirs(
                os.path.dirname(full_path),
                exist_ok=True
            )

            self.tools.write_file(path, content)

        # -----------------------------
        # Save next step
        # -----------------------------
        next_task = data.get("next_task")

        if next_task:
            self.memory.update_knowledge(
                project,
                "next_task",
                next_task
            )

        return {
            "project": project,
            "fix_mode": fix_mode,
            "files_updated": list(files.keys()),
            "next_task": next_task
        }

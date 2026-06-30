import json
import os

from agents.base_agent import BaseAgent
from core.task import Task
from core.project_indexer import ProjectIndexer
from core.code_memory import CodeMemory
from core.agent_debate import AgentDebateSystem


class CoderAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)

        self.indexer = ProjectIndexer()
        self.code_memory = CodeMemory()
        self.debate = AgentDebateSystem(llm)

    def can_handle(self, task: Task):
        return task.task_type == "code"

    def execute(self, task: Task):

        project = task.data.get("project")
        fix_mode = task.data.get("mode") == "fix"
        errors = task.data.get("errors")
        structure = task.data.get("structure")

        # -----------------------------
        # Build structural context
        # -----------------------------
        index = self.indexer.build_index("workspace")

        plan = self.memory.load_plan(project)

        # -----------------------------
        # SMART RETRIEVAL (RAG LAYER)
        # -----------------------------
        keywords = self._extract_keywords(plan, errors)

        relevant_files = self.code_memory.retrieve_relevant_files(keywords)

        retrieved_context = json.dumps(relevant_files, indent=2)

        # -----------------------------
        # MULTI-MODE REASONING INPUT
        # -----------------------------
        base_prompt = f"""
You are an expert software engineer working in a real codebase.

PROJECT PLAN:
{json.dumps(plan, indent=2)}

STRUCTURE:
{json.dumps(index, indent=2)}

RETRIEVED CONTEXT (most relevant existing code):
{retrieved_context}

ERRORS:
{json.dumps(errors, indent=2)}

FIX MODE: {fix_mode}

RULES:
- You may assume code will be executed in a real runtime
- Ensure dependencies are installable
- Ensure main.py can run directly
- Avoid broken imports
- Keep system runnable at all times

Return ONLY valid JSON:
{{
  "files": {{
    "path/to/file.py": "code"
  }},
  "next_task": "test"
}}
"""

        # -----------------------------
        # DEBATE SYSTEM (reasoning upgrade)
        # -----------------------------
        response = self.debate.run_debate(base_prompt)

        try:
            data = json.loads(response)
        except Exception:
            return {
                "error": "Invalid JSON from debate system",
                "raw": response
            }

        files = data.get("files", {})

        # -----------------------------
        # WRITE FILES
        # -----------------------------
        for path, content in files.items():

            full_path = os.path.join("workspace", path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            self.tools.write_file(path, content)

        # -----------------------------
        # MEMORY UPDATE
        # -----------------------------
        self.memory.update_knowledge(
            project,
            "last_code",
            data
        )

        return {
            "project": project,
            "files_updated": list(files.keys())
        }

    # -----------------------------
    # KEYWORD EXTRACTION (simple but effective)
    # -----------------------------
    def _extract_keywords(self, plan, errors):

        keywords = []

        if isinstance(plan, dict):
            keywords += plan.get("architecture", [])
            keywords += plan.get("files_to_create", [])

        if errors:
            if isinstance(errors, dict):
                keywords += list(errors.keys())
                keywords += str(errors).split()

        # cleanup
        return list(set([str(k).lower() for k in keywords if k]))

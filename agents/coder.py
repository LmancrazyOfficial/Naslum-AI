import json
import os

from agents.base_agent import BaseAgent
from core.task import Task
from core.project_indexer import ProjectIndexer
from core.code_memory import CodeMemory
from core.agent_debate import AgentDebateSystem
from core.context_kernel import ContextKernel


class CoderAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):

        super().__init__(name, llm, tools, memory)

        self.indexer = ProjectIndexer()
        self.code_memory = CodeMemory()
        self.debate = AgentDebateSystem(llm)

        # 🧠 NEW: Context OS layer
        self.context_kernel = ContextKernel(memory, self.code_memory)

    # -----------------------------
    # TASK HANDLING
    # -----------------------------
    def can_handle(self, task: Task):
        return task.task_type == "code"

    # -----------------------------
    # MAIN EXECUTION
    # -----------------------------
    def execute(self, task: Task):

        project = task.data.get("project")
        fix_mode = task.data.get("mode") == "fix"
        errors = task.data.get("errors")

        # -----------------------------
        # Build structured index (lightweight structure view)
        # -----------------------------
        index = self.indexer.build_index("workspace")

        plan = self.memory.load_plan(project)

        # -----------------------------
        # 🧠 CONTEXT OS (NEW CORE UPGRADE)
        # -----------------------------
        context = self.context_kernel.build_context(project, task.data)

        # -----------------------------
        # MULTI-AGENT DEBATE (REASONING LAYER)
        # -----------------------------
        prompt = f"""
You are a senior autonomous software engineer working in a live codebase.

========================
PROJECT PLAN
========================
{json.dumps(plan, indent=2)}

========================
PROJECT STRUCTURE
========================
{json.dumps(index, indent=2)}

========================
COMPRESSED MEMORY
========================
{json.dumps(context["memory"], indent=2)}

========================
RETRIEVED CODE (RAG)
========================
{json.dumps(context["retrieved_code"], indent=2)}

========================
TASK
========================
{json.dumps(task.data, indent=2)}

========================
ERRORS (if any)
========================
{json.dumps(errors, indent=2)}

RULES:
- Reuse existing code whenever possible
- Do NOT duplicate functionality already present
- Prefer modifying existing modules over creating new ones
- Ensure consistency across the entire codebase
- Ensure final system is runnable

Return ONLY valid JSON:

{
  "files": {
    "path/to/file.py": "full file content"
  }
}
"""

        response = self.debate.run_debate(prompt)

        # -----------------------------
        # SAFE PARSE
        # -----------------------------
        try:
            data = json.loads(response)
        except Exception:
            return {
                "error": "Invalid JSON from coder/debate system",
                "raw": response
            }

        files = data.get("files", {})

        # -----------------------------
        # WRITE FILES TO WORKSPACE
        # -----------------------------
        for path, content in files.items():

            full_path = os.path.join("workspace", path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            self.tools.write_file(path, content)

        # -----------------------------
        # STORE RESULT IN MEMORY
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

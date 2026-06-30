import json
import os

from agents.base_agent import BaseAgent
from core.task import Task
from core.project_indexer import ProjectIndexer
from core.agent_debate import AgentDebateSystem


class CoderAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)
        self.indexer = ProjectIndexer()
        self.debate = AgentDebateSystem(llm)

    def can_handle(self, task: Task):
        return task.task_type == "code"

    def execute(self, task: Task):

        project = task.data.get("project")
        fix_mode = task.data.get("mode") == "fix"
        errors = task.data.get("errors")

        project_path = "workspace"
        index = self.indexer.build_index(project_path)

        plan = self.memory.load_plan(project)

        base_prompt = f"""
PROJECT PLAN:
{json.dumps(plan, indent=2)}

PROJECT STRUCTURE:
{json.dumps(index, indent=2)}

FIX MODE: {fix_mode}
ERRORS: {json.dumps(errors, indent=2)}
"""

        # -----------------------------
        # MULTI-AGENT DEBATE STEP
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

        for path, content in files.items():

            full_path = os.path.join("workspace", path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            self.tools.write_file(path, content)

        self.memory.update_knowledge(
            project,
            "last_code",
            data
        )

        return {
            "project": project,
            "files_updated": list(files.keys())
        }

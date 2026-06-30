from agents.base_agent import BaseAgent
from core.task import Task

import os
import hashlib


class AnalyzerAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)

    def can_handle(self, task: Task):
        return task.task_type == "analyze"

    def execute(self, task: Task):

        project_path = task.data.get("project_path", "workspace")

        project = {
            "files": [],
            "summary": {}
        }

        total_lines = 0

        for root, dirs, files in os.walk(project_path):

            for filename in files:

                full_path = os.path.join(root, filename)

                relative = os.path.relpath(full_path, project_path)

                try:

                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    lines = len(content.splitlines())

                    total_lines += lines

                    file_info = {
                        "path": relative,
                        "lines": lines,
                        "size": len(content),
                        "sha256": hashlib.sha256(
                            content.encode("utf-8")
                        ).hexdigest(),
                        "preview": content[:500]
                    }

                    project["files"].append(file_info)

                except Exception as e:

                    project["files"].append({
                        "path": relative,
                        "error": str(e)
                    })

        project["summary"] = {
            "total_files": len(project["files"]),
            "total_lines": total_lines
        }

        self.memory.add_knowledge(
            "last_analysis",
            project
        )

        return project

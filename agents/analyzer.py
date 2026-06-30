from agents.base_agent import BaseAgent
from core.task import Task
from core.git_manager import GitManager


class AnalyzerAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)
        self.git = GitManager()

    def can_handle(self, task: Task):
        return task.task_type == "analyze"

    def execute(self, task: Task):

        project = task.data.get("project")

        diff = self.git.diff()
        log = self.git.log()

        analysis = {
            "diff": diff,
            "history": log
        }

        # store analysis
        self.memory.update_knowledge(
            project,
            "analysis",
            analysis
        )

        return analysis

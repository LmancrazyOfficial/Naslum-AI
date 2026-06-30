from agents.base_agent import BaseAgent
from core.task import Task
from core.tool_executor import ToolExecutor


class TesterAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):
        super().__init__(name, llm, tools, memory)
        self.executor = ToolExecutor()

    def can_handle(self, task: Task):
        return task.task_type == "test"

    def execute(self, task: Task):

        project = task.data.get("project")

        # Try running main entry
        result = self.executor.run_command("python main.py")

        test_result = {
            "success": result["success"],
            "output": result["output"],
            "error": result["error"]
        }

        self.memory.update_knowledge(
            project,
            "last_test",
            test_result
        )

        self.memory.append_history(
            project,
            {
                "event": "real_test_execution",
                "success": result["success"]
            }
        )

        return test_result

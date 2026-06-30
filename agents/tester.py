from agents.base_agent import BaseAgent
from core.task import Task
from core.tool_executor import ToolExecutor
from core.runtime_analyzer import RuntimeAnalyzer
from core.code_memory import CodeMemory


class TesterAgent(BaseAgent):

    def __init__(self, name, llm, tools, memory):

        super().__init__(name, llm, tools, memory)

        self.executor = ToolExecutor()
        self.analyzer = RuntimeAnalyzer(llm)
        self.code_memory = CodeMemory()

    def can_handle(self, task: Task):
        return task.task_type == "test"

    def execute(self, task: Task):

        project = task.data.get("project")

        # -----------------------------
        # RUN SYSTEM
        # -----------------------------
        result = self.executor.run_command("python main.py")

        error_context = {
            "success": result["success"],
            "stdout": result["output"],
            "stderr": result["error"]
        }

        # -----------------------------
        # IF ERROR → INTELLIGENT ANALYSIS
        # -----------------------------
        if not result["success"]:

            code_context = self.code_memory.retrieve_relevant_files(
                ["main", "error", "app", "server", "index"]
            )

            analysis = self.analyzer.analyze_error(
                error_context,
                code_context
            )

        else:
            analysis = {
                "status": "success",
                "message": "No runtime errors"
            }

        # -----------------------------
        # STORE RESULTS
        # -----------------------------
        self.memory.update_knowledge(
            project,
            "last_test",
            {
                "runtime_result": error_context,
                "analysis": analysis
            }
        )

        self.memory.append_history(
            project,
            {
                "event": "runtime_test",
                "success": result["success"]
            }
        )

        return {
            "success": result["success"],
            "analysis": analysis
        }

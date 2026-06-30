from core.task_queue import TaskQueue
from core.task import Task
from core.agent_registry import AgentRegistry

from core.execution_engine import ExecutionEngine
from core.tool_manager import ToolManager

from memory.memory_manager import MemoryManager

from llm.local_model import LocalModel

from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from agents.analyzer import AnalyzerAgent


class Orchestrator:

    def __init__(self):

        self.llm = LocalModel()
        self.tools = ToolManager()
        self.memory = MemoryManager()

        self.queue = TaskQueue()
        self.registry = AgentRegistry()

        self.engine = ExecutionEngine(self)

        self._register_agents()

    def _register_agents(self):

        self.registry.register(
            PlannerAgent("Planner", self.llm, self.tools, self.memory)
        )

        self.registry.register(
            CoderAgent("Coder", self.llm, self.tools, self.memory)
        )

        self.registry.register(
            TesterAgent("Tester", self.llm, self.tools, self.memory)
        )

        self.registry.register(
            AnalyzerAgent("Analyzer", self.llm, self.tools, self.memory)
        )

    # -----------------------------
    # Task system
    # -----------------------------

    def submit_task(self, task_type, data):

        task = Task(
            task_type=task_type,
            data=data
        )

        self.queue.add_task(task)

    def process_tasks(self):

        while self.queue.has_tasks():

            task = self.queue.get_task()

            agent = self.registry.find_agent(task)

            if agent is None:
                print(f"[WARN] No agent for: {task.task_type}")
                continue

            print(f"[{agent.name}] -> {task.task_type}")

            try:
                result = agent.execute(task)

                task.status = "completed"
                task.result = result

            except Exception as e:

                task.status = "failed"
                task.error = str(e)

                print(f"[ERROR] {e}")

    # -----------------------------
    # Entry point
    # -----------------------------

    def run(self, user_request):

        print("\n" + "=" * 60)
        print("AI FACTORY RUNNING")
        print("=" * 60)

        # Create project name from request
        project_name = "project_" + str(abs(hash(user_request)))[:8]

        self.memory.create_project(project_name)

        self.memory.append_history(
            project_name,
            {"request": user_request}
        )

        # Store project context in engine
        self.engine.execute_project(
            request=user_request,
            project=project_name
        )

        print("\nDONE")

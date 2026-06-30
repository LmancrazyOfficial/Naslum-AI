from core.agent_registry import AgentRegistry
from core.task_queue import TaskQueue
from core.task import Task

from core.tool_manager import ToolManager
from memory.memory_manager import MemoryManager

from llm.local_model import LocalModel

from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from agents.analyzer import AnalyzerAgent


class Orchestrator:
    def __init__(self):

        # Core systems
        self.llm = LocalModel()
        self.tools = ToolManager()
        self.memory = MemoryManager()

        # Task system
        self.queue = TaskQueue()
        self.registry = AgentRegistry()

        # Register agents
        self.registry.register(
            PlannerAgent(
                "Planner",
                self.llm,
                self.tools,
                self.memory
            )
        )

        self.registry.register(
            CoderAgent(
                "Coder",
                self.llm,
                self.tools,
                self.memory
            )
        )

        self.registry.register(
            TesterAgent(
                "Tester",
                self.llm,
                self.tools,
                self.memory
            )
        )

        self.registry.register(
            AnalyzerAgent(
                "Analyzer",
                self.llm,
                self.tools,
                self.memory
            )
        )

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
                print(f"No agent found for task '{task.task_type}'")
                continue

            print(f"[{agent.name}] Processing {task.task_type}")

            try:

                result = agent.execute(task)

                task.status = "completed"
                task.result = result

            except Exception as e:

                task.status = "failed"
                task.error = str(e)

                print(f"Task failed: {e}")

    def run(self, user_request):

        print("\n========== AI FACTORY ==========")

        self.memory.add_task(user_request)

        self.submit_task(
            "plan",
            {
                "request": user_request
            }
        )

        self.process_tasks()

        print("\n========== DONE ==========")

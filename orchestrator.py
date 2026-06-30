from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from llm.local_model import LocalModel

class Orchestrator:
    def __init__(self):
        self.llm = LocalModel()

        self.planner = PlannerAgent(self.llm)
        self.coder = CoderAgent(self.llm)
        self.tester = TesterAgent()

    def run(self, task: str):
        plan = self.planner.create_plan(task)
        code = self.coder.generate_code(plan)
        test = self.tester.run_code(code)

        return {
            "plan": plan,
            "code": code,
            "test": test
        }

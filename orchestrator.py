from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.coder = CoderAgent()
        self.tester = TesterAgent()

    def run(self, task: str):
        print("\n[1] Planning...")
        plan = self.planner.create_plan(task)

        print("\n[2] Coding...")
        code_output = self.coder.generate_code(plan)

        print("\n[3] Testing...")
        test_result = self.tester.run_code(code_output)

        return {
            "plan": plan,
            "code": code_output,
            "test": test_result
        }

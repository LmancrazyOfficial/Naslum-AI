class PlannerAgent:
    def create_plan(self, task: str):
        return {
            "task": task,
            "steps": [
                "Define structure",
                "Generate code files",
                "Run tests"
            ]
        }

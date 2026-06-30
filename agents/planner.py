class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, task: str):
        prompt = f"""
Break this into a software architecture plan:

Task: {task}

Return JSON:
- goal
- steps
- files needed
"""

        return self.llm.generate(prompt)

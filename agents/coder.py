class CoderAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_code(self, plan):
        prompt = f"""
You are a senior software engineer.

Based on this plan:
{plan}

Generate a complete working Python project.
Return as file map:
- filename: code
"""

        return self.llm.generate(prompt)

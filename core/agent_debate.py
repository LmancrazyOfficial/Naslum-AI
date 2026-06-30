import json


class AgentDebateSystem:

    def __init__(self, llm):
        self.llm = llm

    def run_debate(self, prompt):

        roles = {
            "architect": self._ask_architect(prompt),
            "reviewer": self._ask_reviewer(prompt),
            "optimizer": self._ask_optimizer(prompt)
        }

        final = self._synthesize(prompt, roles)

        return final

    # -----------------------------
    # Individual roles
    # -----------------------------

    def _ask_architect(self, prompt):

        return self.llm.generate(f"""
You are a SOFTWARE ARCHITECT.

Design the best possible solution.

TASK:
{prompt}

Return structured JSON.
""")

    def _ask_reviewer(self, prompt):

        return self.llm.generate(f"""
You are a CODE REVIEWER.

Find flaws, bugs, missing edge cases, and risks.

TASK:
{prompt}

Return structured JSON critique.
""")

    def _ask_optimizer(self, prompt):

        return self.llm.generate(f"""
You are a PERFORMANCE OPTIMIZER.

Improve architecture, reduce complexity, increase efficiency.

TASK:
{prompt}

Return improved structured JSON.
""")

    # -----------------------------
    # Final synthesis
    # -----------------------------

    def _synthesize(self, prompt, roles):

        return self.llm.generate(f"""
You are the FINAL ENGINEER.

Combine the best parts of these perspectives:

ARCHITECT:
{roles['architect']}

REVIEWER:
{roles['reviewer']}

OPTIMIZER:
{roles['optimizer']}

TASK:
{prompt}

Return the FINAL correct JSON solution only.
""")

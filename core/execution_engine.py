from core.goal_decomposer import GoalDecomposer
from core.self_improver import SelfImprover
from core.meta_controller import MetaController


class ExecutionEngine:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator

        self.decomposer = GoalDecomposer(orchestrator.llm)
        self.improver = SelfImprover(orchestrator.llm, orchestrator.memory)
        self.meta = MetaController(orchestrator.llm, orchestrator.memory)

        self.max_retries = 2

    def execute_project(self, request, project):

        # -----------------------------
        # 0. META STRATEGY EVOLUTION (NEW CORE LAYER)
        # -----------------------------
        strategy_update =

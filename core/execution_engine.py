from core.goal_decomposer import GoalDecomposer
from core.self_improver import SelfImprover
from core.meta_controller import MetaController
from core.mission_manager import MissionManager
from core.swarm_coordinator import SwarmCoordinator


class ExecutionEngine:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator

        self.decomposer = GoalDecomposer(orchestrator.llm)
        self.improver = SelfImprover(orchestrator.llm, orchestrator.memory)
        self.meta = MetaController(orchestrator.llm, orchestrator.memory)
        self.missions = MissionManager()

        # 🧠 SWARM MODE ENABLED
        self.swarm = SwarmCoordinator(orchestrator.agents)

        self.max_retries = 2

    def execute_project(self, request, project):

        mission = self.missions.create_mission(request)
        mission_id = mission["id"]

        # -----------------------------
        # 0. DECOMPOSE GOAL
        # -----------------------------
        structure = self.decomposer.decompose(request)

        self.orchestrator.memory.update_knowledge(
            project,
            "goal_structure",
            structure
        )

        # -----------------------------
        # 1. BUILD TASK LIST FROM STRUCTURE
        # -----------------------------
        tasks = []

        for module in structure.get("modules", []):

            tasks.append({
                "task_type": "code",
                "project": project,
                "module": module
            })

        # -----------------------------
        # 2. SWARM EXECUTION (PARALLELIZED CODING)
        # -----------------------------
        code_results = self.swarm.distribute(tasks)

        self.missions.update_mission(
            mission_id,
            "Swarm coding complete"
        )

        # -----------------------------
        # 3. TESTING PHASE
        # -----------------------------
        test_tasks = [{
            "task_type": "test",
            "project": project
        }]

        test_results = self.swarm.distribute(test_tasks)

        success = any(r.get("success") for r in test_results)

        # -----------------------------
        # 4. ANALYSIS
        # -----------------------------
        self.swarm.distribute([{
            "task_type": "analyze",
            "project": project
        }])

        # -----------------------------
        # 5. SELF IMPROVEMENT
        # -----------------------------
        insights = self.improver.analyze_project(project)

        self.orchestrator.memory.update_knowledge(
            project,
            "insights",
            insights
        )

        self.orchestrator.memory.global_memory.store_insight(insights)

        self.missions.complete_mission(mission_id)

        return {
            "project": project,
            "mission_id": mission_id,
            "success": success,
            "swarm_results": code_results,
            "insights": insights
        }

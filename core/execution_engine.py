from core.goal_decomposer import GoalDecomposer
from core.self_improver import SelfImprover
from core.meta_controller import MetaController
from core.mission_manager import MissionManager
from core.swarm_coordinator import SwarmCoordinator
from core.goal_generator import GoalGenerator


class ExecutionEngine:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator

        self.decomposer = GoalDecomposer(orchestrator.llm)
        self.improver = SelfImprover(orchestrator.llm, orchestrator.memory)
        self.meta = MetaController(orchestrator.llm, orchestrator.memory)

        self.missions = MissionManager()
        self.goal_generator = GoalGenerator(orchestrator.llm, orchestrator.memory)

        # Swarm system (multi-agent execution)
        self.swarm = SwarmCoordinator(orchestrator.agents)

        self.max_retries = 2

    # -----------------------------
    # MAIN ENTRY POINT
    # -----------------------------
    def execute_project(self, request, project):

        # -----------------------------
        # 0. CREATE MISSION
        # -----------------------------
        mission = self.missions.create_mission(request)
        mission_id = mission["id"]

        # -----------------------------
        # 1. META STRATEGY STEP (optional hook)
        # -----------------------------
        strategy_update = self.meta.evolve_strategy()

        self.orchestrator.memory.update_knowledge(
            project,
            "strategy_update",
            strategy_update
        )

        # -----------------------------
        # 2. GOAL DECOMPOSITION
        # -----------------------------
        structure = self.decomposer.decompose(request)

        self.orchestrator.memory.update_knowledge(
            project,
            "goal_structure",
            structure
        )

        self.missions.update_mission(
            mission_id,
            "Goal decomposed"
        )

        # -----------------------------
        # 3. BUILD SWARM TASKS
        # -----------------------------
        tasks = []

        for module in structure.get("modules", []):

            tasks.append({
                "task_type": "code",
                "project": project,
                "module": module
            })

        # -----------------------------
        # 4. SWARM CODING EXECUTION
        # -----------------------------
        code_results = self.swarm.distribute(tasks)

        self.missions.update_mission(
            mission_id,
            "Swarm coding complete"
        )

        # -----------------------------
        # 5. TEST PHASE (SWARM)
        # -----------------------------
        test_results = self.swarm.distribute([
            {
                "task_type": "test",
                "project": project
            }
        ])

        success = any(
            r.get("success") for r in test_results if isinstance(r, dict)
        )

        # -----------------------------
        # 6. ANALYSIS PHASE
        # -----------------------------
        self.swarm.distribute([
            {
                "task_type": "analyze",
                "project": project
            }
        ])

        # -----------------------------
        # 7. SELF-IMPROVEMENT
        # -----------------------------
        insights = self.improver.analyze_project(project)

        self.orchestrator.memory.update_knowledge(
            project,
            "insights",
            insights
        )

        self.orchestrator.memory.global_memory.store_insight(insights)

        # -----------------------------
        # 8. MISSION COMPLETION
        # -----------------------------
        self.missions.complete_mission(mission_id)

        # -----------------------------
        # 9. AUTONOMOUS GOAL GENERATION
        # -----------------------------
        new_goals = self.goal_generator.generate_goals()

        if new_goals and "new_goals" in new_goals:

            self.missions.add_auto_missions(new_goals["new_goals"])

            self.orchestrator.memory.update_knowledge(
                project,
                "auto_generated_goals",
                new_goals
            )

        # -----------------------------
        # FINAL OUTPUT
        # -----------------------------
        return {
            "project": project,
            "mission_id": mission_id,
            "success": success,
            "structure": structure,
            "code_results": code_results,
            "test_results": test_results,
            "insights": insights,
            "strategy_update": strategy_update,
            "auto_goals": new_goals
        }

from core.goal_decomposer import GoalDecomposer
from core.self_improver import SelfImprover
from core.meta_controller import MetaController
from core.mission_manager import MissionManager


class ExecutionEngine:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator

        self.decomposer = GoalDecomposer(orchestrator.llm)
        self.improver = SelfImprover(orchestrator.llm, orchestrator.memory)
        self.meta = MetaController(orchestrator.llm, orchestrator.memory)
        self.missions = MissionManager()

        self.max_retries = 2

    # -----------------------------
    # ENTRY POINT (NOW MISSION-BASED)
    # -----------------------------

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

        self.missions.update_mission(
            mission_id,
            "Goal decomposed"
        )

        # -----------------------------
        # 1. PLAN
        # -----------------------------
        self.orchestrator.submit_task("plan", {
            "request": request,
            "project": project,
            "structure": structure
        })
        self.orchestrator.process_tasks()

        self.missions.update_mission(mission_id, "Planning complete")

        # -----------------------------
        # 2. CODE
        # -----------------------------
        self.orchestrator.submit_task("code", {
            "project": project,
            "structure": structure
        })
        self.orchestrator.process_tasks()

        self.missions.update_mission(mission_id, "Coding complete")

        # -----------------------------
        # 3. TEST + FIX LOOP
        # -----------------------------
        retries = 0
        success = False

        while retries <= self.max_retries:

            self.orchestrator.submit_task("test", {"project": project})
            self.orchestrator.process_tasks()

            test_result = self.orchestrator.memory.get_knowledge(
                project,
                "last_test"
            )

            if test_result and test_result.get("success"):
                success = True
                break

            self.orchestrator.submit_task("code", {
                "project": project,
                "mode": "fix",
                "errors": test_result,
                "structure": structure
            })
            self.orchestrator.process_tasks()

            retries += 1

            self.missions.update_mission(
                mission_id,
                f"Fix cycle {retries}"
            )

        # -----------------------------
        # 4. ANALYZE
        # -----------------------------
        self.orchestrator.submit_task("analyze", {
            "project": project,
            "structure": structure
        })
        self.orchestrator.process_tasks()

        self.missions.update_mission(
            mission_id,
            "Analysis complete"
        )

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

        self.missions.update_mission(
            mission_id,
            "Self-improvement complete"
        )

        self.missions.complete_mission(mission_id)

        return {
            "project": project,
            "mission_id": mission_id,
            "success": success,
            "structure": structure,
            "insights": insights
        }

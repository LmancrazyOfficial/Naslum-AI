from core.goal_decomposer import GoalDecomposer


class ExecutionEngine:

    def __init__(self, orchestrator):

        self.orchestrator = orchestrator
        self.decomposer = GoalDecomposer(orchestrator.llm)

        self.max_retries = 2

    # -----------------------------
    # ENTRY
    # -----------------------------

    def execute_project(self, request, project):

        # -----------------------------
        # 0. GOAL DECOMPOSITION (NEW)
        # -----------------------------
        structure = self.decomposer.decompose(request)

        self.orchestrator.memory.update_knowledge(
            project,
            "goal_structure",
            structure
        )

        # -----------------------------
        # 1. PLAN
        # -----------------------------
        self.orchestrator.submit_task(
            "plan",
            {
                "request": request,
                "project": project,
                "structure": structure
            }
        )
        self.orchestrator.process_tasks()

        # -----------------------------
        # 2. CODE
        # -----------------------------
        self.orchestrator.submit_task(
            "code",
            {
                "project": project,
                "structure": structure
            }
        )
        self.orchestrator.process_tasks()

        # -----------------------------
        # 3. TEST + FIX LOOP
        # -----------------------------
        retries = 0
        success = False

        while retries <= self.max_retries:

            self.orchestrator.submit_task(
                "test",
                {
                    "project": project
                }
            )

            self.orchestrator.process_tasks()

            test_result = self.orchestrator.memory.get_knowledge(
                project,
                "last_test"
            )

            if test_result and test_result.get("success"):
                success = True
                break

            self.orchestrator.submit_task(
                "code",
                {
                    "project": project,
                    "mode": "fix",
                    "errors": test_result,
                    "structure": structure
                }
            )

            self.orchestrator.process_tasks()

            retries += 1

        # -----------------------------
        # 4. ANALYZE
        # -----------------------------
        self.orchestrator.submit_task(
            "analyze",
            {
                "project": project,
                "structure": structure
            }
        )
        self.orchestrator.process_tasks()

        return {
            "project": project,
            "success": success,
            "structure": structure
        }

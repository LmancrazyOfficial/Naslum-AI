class ExecutionEngine:

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.max_retries = 2

    def execute_project(self, request, project):

        # -------------------------
        # STEP 1: PLAN
        # -------------------------
        self.orchestrator.submit_task(
            "plan",
            {
                "request": request,
                "project": project
            }
        )
        self.orchestrator.process_tasks()

        # -------------------------
        # STEP 2: CODE (initial build)
        # -------------------------
        self.orchestrator.submit_task(
            "code",
            {
                "project": project,
                "mode": "initial"
            }
        )
        self.orchestrator.process_tasks()

        # -------------------------
        # STEP 3: TEST + FIX LOOP
        # -------------------------
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

            # FIX STEP
            self.orchestrator.submit_task(
                "code",
                {
                    "project": project,
                    "mode": "fix",
                    "errors": test_result
                }
            )

            self.orchestrator.process_tasks()

            retries += 1

        # -------------------------
        # FINAL ANALYSIS
        # -------------------------
        self.orchestrator.submit_task(
            "analyze",
            {
                "project": project
            }
        )

        self.orchestrator.process_tasks()

        return {
            "project": project,
            "success": success,
            "retries": retries
        }

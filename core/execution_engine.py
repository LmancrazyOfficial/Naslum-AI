class ExecutionEngine:

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.max_retries = 2

    def execute_project(self, request):

        # 1. PLAN
        self.orchestrator.submit_task(
            "plan",
            {"request": request}
        )
        self.orchestrator.process_tasks()

        # 2. CODE
        self.orchestrator.submit_task(
            "code",
            {}
        )
        self.orchestrator.process_tasks()

        # 3. TEST + RETRY LOOP
        retries = 0
        success = False

        while retries <= self.max_retries and not success:

            self.orchestrator.submit_task(
                "test",
                {}
            )

            self.orchestrator.process_tasks()

            # Get latest test result from memory
            test_result = self.orchestrator.memory.get_knowledge(
                "default",
                "last_test"
            )

            if test_result and test_result.get("success"):
                success = True
                break

            # If failed → FIX
            self.orchestrator.submit_task(
                "code",
                {
                    "fix_mode": True,
                    "errors": test_result
                }
            )

            self.orchestrator.process_tasks()

            retries += 1

        return {
            "success": success,
            "retries": retries
          }

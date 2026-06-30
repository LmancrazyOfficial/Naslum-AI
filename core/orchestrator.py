class Orchestrator:

    def __init__(self, planner, coder, tester, analyzer):
        self.planner = planner
        self.coder = coder
        self.tester = tester
        self.analyzer = analyzer

    def run(self, task, workspace_path):

        plan = self.planner.create_plan(task)

        project_files = self.coder.generate_project(plan, workspace_path)

        for attempt in range(5):  # SELF-IMPROVEMENT LOOP

            result = self.tester.run_project(workspace_path)

            if result["success"]:
                return {
                    "status": "success",
                    "output": result
                }

            analysis = self.analyzer.scan_project(workspace_path)

            fix_prompt = {
                "plan": plan,
                "errors": result["stderr"],
                "analysis": analysis
            }

            project_files = self.coder.fix_code(fix_prompt, workspace_path)

        return {
            "status": "failed_after_retries",
            "last_result": result
        }

from core.git_manager import GitManager


class ToolExecutor:

    def __init__(self, workspace="workspace"):
        self.workspace = workspace
        self.git = GitManager(workspace)
        self.git.init_repo()

    def run_command(self, command):

        blocked = ["rm -rf", "shutdown", "reboot", ":(){", "mkfs"]

        if any(b in command for b in blocked):
            return {
                "success": False,
                "error": "Blocked unsafe command",
                "output": ""
            }

        import subprocess
        import shlex

        try:
            result = subprocess.run(
                shlex.split(command),
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=15
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }

        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }

import subprocess
import os


class GitManager:

    def __init__(self, workspace="workspace"):
        self.workspace = workspace

    def init_repo(self):

        if not os.path.exists(os.path.join(self.workspace, ".git")):

            subprocess.run(
                ["git", "init"],
                cwd=self.workspace
            )

    def commit_all(self, message):

        try:
            subprocess.run(["git", "add", "."], cwd=self.workspace)

            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def diff(self):

        result = subprocess.run(
            ["git", "diff"],
            cwd=self.workspace,
            capture_output=True,
            text=True
        )

        return result.stdout

    def log(self):

        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=self.workspace,
            capture_output=True,
            text=True
        )

        return result.stdout

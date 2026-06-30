import subprocess
import os
import sys
import tempfile


class Sandbox:

    def __init__(self):
        self.workspace = "workspace"

    def run_python_file(self, file_path):

        full_path = os.path.join(self.workspace, file_path)

        if not os.path.exists(full_path):
            return {
                "success": False,
                "error": "File does not exist",
                "output": ""
            }

        try:
            result = subprocess.run(
                [sys.executable, full_path],
                capture_output=True,
                text=True,
                timeout=10
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Execution timed out"
            }

        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }

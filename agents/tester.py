import subprocess
import tempfile
import os

class TesterAgent:
    def run_code(self, code_files):
        try:
            with tempfile.TemporaryDirectory() as tmp:
                file_path = os.path.join(tmp, "main.py")

                with open(file_path, "w") as f:
                    f.write(code_files["main.py"])

                result = subprocess.run(
                    ["python", file_path],
                    capture_output=True,
                    text=True
                )

                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }

        except Exception as e:
            return {"error": str(e)}

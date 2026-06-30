import subprocess
import os

class SandboxRunner:

    def run_python(self, file_path):
        return subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True
        )

    def run_node(self, file_path):
        return subprocess.run(
            ["node", file_path],
            capture_output=True,
            text=True
        )

    def run_cpp(self, file_path):
        exe = file_path.replace(".cpp", ".out")

        compile = subprocess.run(
            ["g++", file_path, "-o", exe],
            capture_output=True,
            text=True
        )

        if compile.returncode != 0:
            return compile

        return subprocess.run(
            [exe],
            capture_output=True,
            text=True
        )

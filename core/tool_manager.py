import os
import subprocess
from pathlib import Path


class ToolManager:
    def __init__(self, workspace="workspace"):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)

    def read_file(self, relative_path):
        path = self.workspace / relative_path

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, relative_path, content):
        path = self.workspace / relative_path

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return True

    def list_files(self):
        files = []

        for root, _, filenames in os.walk(self.workspace):
            for file in filenames:
                full = Path(root) / file
                files.append(str(full.relative_to(self.workspace)))

        return sorted(files)

    def create_folder(self, relative_path):
        path = self.workspace / relative_path
        path.mkdir(parents=True, exist_ok=True)

    def delete_file(self, relative_path):
        path = self.workspace / relative_path

        if path.exists():
            path.unlink()

    def run_command(self, command):
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.workspace,
            capture_output=True,
            text=True
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

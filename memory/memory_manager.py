import os
import json
from datetime import datetime

from memory.global_memory import GlobalMemory


class MemoryManager:

    def __init__(self):

        self.root = "memory"
        self.projects_root = os.path.join(self.root, "projects")

        os.makedirs(self.projects_root, exist_ok=True)

        self.global_memory = GlobalMemory()

    # -----------------------------
    # helpers
    # -----------------------------

    def _write_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _read_json(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _project_path(self, project):
        return os.path.join(self.projects_root, project)

    # -----------------------------
    # project lifecycle
    # -----------------------------

    def create_project(self, name):

        path = self._project_path(name)

        os.makedirs(path, exist_ok=True)

        for file, data in {
            "metadata.json": {"name": name},
            "plan.json": {},
            "history.json": [],
            "knowledge.json": {},
            "patterns.json": []
        }.items():

            full = os.path.join(path, file)

            if not os.path.exists(full):
                self._write_json(full, data)

        return path

    # -----------------------------
    # knowledge
    # -----------------------------

    def update_knowledge(self, project, key, value):

        path = os.path.join(
            self._project_path(project),
            "knowledge.json"
        )

        data = self._read_json(path)
        data[key] = value

        self._write_json(path, data)

    def get_knowledge(self, project, key):

        path = os.path.join(
            self._project_path(project),
            "knowledge.json"
        )

        data = self._read_json(path)
        return data.get(key)

    # -----------------------------
    # global shortcuts
    # -----------------------------

    def global_patterns(self):
        return self.global_memory.get_patterns()

    def global_failures(self):
        return self.global_memory.get_failures()

    def global_insights(self):
        return self.global_memory.get_insights()

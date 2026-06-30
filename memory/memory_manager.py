import os
import json
from datetime import datetime


class MemoryManager:

    def __init__(self):

        self.root = "memory"
        self.projects_root = os.path.join(self.root, "projects")

        os.makedirs(self.projects_root, exist_ok=True)

        self.settings_path = os.path.join(self.root, "settings.json")

        if not os.path.exists(self.settings_path):
            self._write_json(self.settings_path, {})

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
    # project setup
    # -----------------------------

    def create_project(self, name):

        path = self._project_path(name)

        os.makedirs(path, exist_ok=True)

        structure = {
            "metadata.json": {
                "name": name,
                "created": datetime.now().isoformat()
            },
            "plan.json": {},
            "analysis.json": {},
            "history.json": [],
            "knowledge.json": {},
            "patterns.json": []   # NEW
        }

        for file, data in structure.items():

            full = os.path.join(path, file)

            if not os.path.exists(full):
                self._write_json(full, data)

        return path

    # -----------------------------
    # plans
    # -----------------------------

    def save_plan(self, project, plan):

        path = os.path.join(
            self._project_path(project),
            "plan.json"
        )

        self._write_json(path, plan)

    def load_plan(self, project):

        path = os.path.join(
            self._project_path(project),
            "plan.json"
        )

        return self._read_json(path)

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
    # history
    # -----------------------------

    def append_history(self, project, event):

        path = os.path.join(
            self._project_path(project),
            "history.json"
        )

        history = self._read_json(path)

        history.append({
            "time": datetime.now().isoformat(),
            "event": event
        })

        self._write_json(path, history)

    # -----------------------------
    # learning layer (NEW)
    # -----------------------------

    def store_pattern(self, project, pattern):

        """
        Store successful solutions or reusable structures.
        """

        path = os.path.join(
            self._project_path(project),
            "patterns.json"
        )

        patterns = self._read_json(path)

        patterns.append({
            "time": datetime.now().isoformat(),
            "pattern": pattern
        })

        self._write_json(path, patterns)

    def get_patterns(self, project):

        path = os.path.join(
            self._project_path(project),
            "patterns.json"
        )

        return self._read_json(path)

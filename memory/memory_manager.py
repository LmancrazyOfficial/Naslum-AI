import os
import json
from datetime import datetime


class MemoryManager:

    def __init__(self):

        self.root = "memory"

        self.projects = os.path.join(self.root, "projects")

        self.conversations = os.path.join(
            self.root,
            "conversations"
        )

        os.makedirs(self.projects, exist_ok=True)
        os.makedirs(self.conversations, exist_ok=True)

        self.settings = os.path.join(
            self.root,
            "settings.json"
        )

        if not os.path.exists(self.settings):
            self._write_json(
                self.settings,
                {}
            )

    def _write_json(self, path, data):

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _read_json(self, path):

        if not os.path.exists(path):
            return {}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_project(self, name):

        project = os.path.join(
            self.projects,
            name
        )

        os.makedirs(project, exist_ok=True)

        files = {

            "metadata.json": {
                "created": datetime.now().isoformat(),
                "name": name
            },

            "plan.json": {},

            "analysis.json": {},

            "history.json": [],

            "knowledge.json": {}

        }

        for filename, data in files.items():

            path = os.path.join(
                project,
                filename
            )

            if not os.path.exists(path):
                self._write_json(path, data)

        return project

    def save_plan(self, project, plan):

        path = os.path.join(
            self.projects,
            project,
            "plan.json"
        )

        self._write_json(path, plan)

    def load_plan(self, project):

        path = os.path.join(
            self.projects,
            project,
            "plan.json"
        )

        return self._read_json(path)

    def save_analysis(self, project, analysis):

        path = os.path.join(
            self.projects,
            project,
            "analysis.json"
        )

        self._write_json(path, analysis)

    def load_analysis(self, project):

        path = os.path.join(
            self.projects,
            project,
            "analysis.json"
        )

        return self._read_json(path)

    def append_history(self, project, event):

        path = os.path.join(
            self.projects,
            project,
            "history.json"
        )

        history = self._read_json(path)

        history.append({

            "time": datetime.now().isoformat(),

            "event": event

        })

        self._write_json(path, history)

    def update_knowledge(
        self,
        project,
        key,
        value
    ):

        path = os.path.join(
            self.projects,
            project,
            "knowledge.json"
        )

        knowledge = self._read_json(path)

        knowledge[key] = value

        self._write_json(path, knowledge)

    def get_knowledge(
        self,
        project,
        key
    ):

        path = os.path.join(
            self.projects,
            project,
            "knowledge.json"
        )

        knowledge = self._read_json(path)

        return knowledge.get(key)

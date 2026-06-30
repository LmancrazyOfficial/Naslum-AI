import json
import os
from datetime import datetime


class MemoryManager:
    def __init__(self, memory_file="memory/state.json"):
        self.memory_file = memory_file

        os.makedirs(os.path.dirname(memory_file), exist_ok=True)

        if not os.path.exists(memory_file):
            self.save({
                "projects": {},
                "recent_tasks": [],
                "settings": {},
                "knowledge": {}
            })

    def load(self):
        with open(self.memory_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_task(self, task):
        data = self.load()

        data["recent_tasks"].append({
            "task": task,
            "time": datetime.now().isoformat()
        })

        # Keep only the last 100 tasks
        data["recent_tasks"] = data["recent_tasks"][-100:]

        self.save(data)

    def save_project(self, project_name, project_data):
        data = self.load()

        data["projects"][project_name] = project_data

        self.save(data)

    def get_project(self, project_name):
        data = self.load()
        return data["projects"].get(project_name)

    def update_setting(self, key, value):
        data = self.load()

        data["settings"][key] = value

        self.save(data)

    def get_setting(self, key, default=None):
        data = self.load()
        return data["settings"].get(key, default)

    def add_knowledge(self, key, value):
        data = self.load()

        data["knowledge"][key] = value

        self.save(data)

    def get_knowledge(self, key):
        data = self.load()
        return data["knowledge"].get(key)

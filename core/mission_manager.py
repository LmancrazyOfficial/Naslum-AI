import os
import json
from datetime import datetime


class MissionManager:

    def __init__(self):

        self.path = "memory/missions.json"

        if not os.path.exists(self.path):
            self._write([])

    def _read(self):

        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data):

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def create_mission(self, goal):

        missions = self._read()

        mission = {
            "id": len(missions) + 1,
            "goal": goal,
            "status": "active",
            "created": datetime.now().isoformat(),
            "progress": []
        }

        missions.append(mission)
        self._write(missions)

        return mission

    def get_active_missions(self):

        return [m for m in self._read() if m["status"] == "active"]

    def update_mission(self, mission_id, update):

        missions = self._read()

        for m in missions:
            if m["id"] == mission_id:
                m["progress"].append({
                    "time": datetime.now().isoformat(),
                    "update": update
                })

        self._write(missions)

    def complete_mission(self, mission_id):

        missions = self._read()

        for m in missions:
            if m["id"] == mission_id:
                m["status"] = "completed"

        self._write(missions)

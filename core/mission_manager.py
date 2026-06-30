def add_auto_missions(self, goals):

    missions = self._read()

    for g in goals:

        mission = {
            "id": len(missions) + 1,
            "goal": g["goal"],
            "status": "active",
            "created": datetime.now().isoformat(),
            "auto_generated": True,
            "reason": g.get("reason"),
            "progress": []
        }

        missions.append(mission)

    self._write(missions)

import json
import os


class Repository:

    def save_index(self, project_path, index):

        output = os.path.join(
            project_path,
            ".ai_index.json"
        )

        with open(output, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)

    def load_index(self, project_path):

        output = os.path.join(
            project_path,
            ".ai_index.json"
        )

        if not os.path.exists(output):
            return None

        with open(output, "r", encoding="utf-8") as f:
            return json.load(f)

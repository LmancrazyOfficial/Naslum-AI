import os

class AnalyzerAgent:
    def scan_project(self, path: str):
        structure = {}

        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", errors="ignore") as f:
                        content = f.read()

                    structure[full_path] = {
                        "lines": len(content.splitlines()),
                        "preview": content[:500]
                    }

                except Exception as e:
                    structure[full_path] = {"error": str(e)}

        return structure

from agents.analyzer import AnalyzerAgent
from sandbox.runner import SandboxRunner
from utils.language_router import detect_language

class Orchestrator:

    def __init__(self):
        self.analyzer = AnalyzerAgent()
        self.runner = SandboxRunner()

    def run_project(self, path):
        analysis = self.analyzer.scan_project(path)

        results = {}

        for file_path in analysis.keys():
            lang = detect_language(file_path)

            if lang == "python":
                results[file_path] = self.runner.run_python(file_path)

            elif lang == "node":
                results[file_path] = self.runner.run_node(file_path)

            elif lang == "cpp":
                results[file_path] = self.runner.run_cpp(file_path)

        return results

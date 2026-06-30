import os
import re
import hashlib
from pathlib import Path


class ProjectIndexer:

    def __init__(self):
        pass

    # -----------------------------
    # Public API
    # -----------------------------

    def build_index(self, project_path):

        project_path = Path(project_path)

        index = {
            "files": {},
            "symbols": {
                "functions": {},
                "classes": {},
                "imports": {}
            },
            "dependencies": {},
            "summary": {
                "total_files": 0,
                "total_lines": 0,
                "languages": {}
            }
        }

        for root, dirs, files in os.walk(project_path):

            dirs[:] = [
                d for d in dirs
                if d not in {
                    ".git",
                    "__pycache__",
                    "node_modules",
                    ".venv",
                    "venv",
                    "dist",
                    "build"
                }
            ]

            for filename in files:

                full_path = Path(root) / filename
                relative = str(full_path.relative_to(project_path))

                try:
                    content = full_path.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )
                except Exception:
                    continue

                lines = content.splitlines()

                file_info = self._analyze_file(
                    content,
                    lines
                )

                file_hash = hashlib.sha256(
                    content.encode("utf-8")
                ).hexdigest()

                index["files"][relative] = {
                    "lines": len(lines),
                    "hash": file_hash,
                    "functions": file_info["functions"],
                    "classes": file_info["classes"],
                    "imports": file_info["imports"]
                }

                # Merge into global symbol map
                self._merge_symbols(index, relative, file_info)

                # Build dependency graph
                index["dependencies"][relative] = file_info["imports"]

                index["summary"]["total_files"] += 1
                index["summary"]["total_lines"] += len(lines)

        return index

    # -----------------------------
    # File analysis
    # -----------------------------

    def _analyze_file(self, content, lines):

        functions = []
        classes = []
        imports = []

        for line in lines:

            line = line.strip()

            # Python function detection
            if line.startswith("def "):
                match = re.match(r"def ([a-zA-Z0-9_]+)", line)
                if match:
                    functions.append(match.group(1))

            # Class detection
            if line.startswith("class "):
                match = re.match(r"class ([a-zA-Z0-9_]+)", line)
                if match:
                    classes.append(match.group(1))

            # Import detection
            if line.startswith("import ") or line.startswith("from "):
                imports.append(line)

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports
        }

    # -----------------------------
    # Symbol merging
    # -----------------------------

    def _merge_symbols(self, index, file_path, file_info):

        for func in file_info["functions"]:
            index["symbols"]["functions"].setdefault(func, [])
            index["symbols"]["functions"][func].append(file_path)

        for cls in file_info["classes"]:
            index["symbols"]["classes"].setdefault(cls, [])
            index["symbols"]["classes"][cls].append(file_path)

        for imp in file_info["imports"]:
            index["symbols"]["imports"].setdefault(imp, [])
            index["symbols"]["imports"][imp].append(file_path)

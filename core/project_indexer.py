import os
import hashlib
from pathlib import Path


class ProjectIndexer:

    def __init__(self):
        pass

    def build_index(self, project_path):

        project_path = Path(project_path)

        index = {
            "files": {},
            "summary": {
                "total_files": 0,
                "total_lines": 0,
                "languages": {}
            }
        }

        language_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript React",
            ".jsx": "React",
            ".cpp": "C++",
            ".c": "C",
            ".h": "C Header",
            ".hpp": "C++ Header",
            ".rs": "Rust",
            ".go": "Go",
            ".java": "Java",
            ".cs": "C#",
            ".php": "PHP",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".html": "HTML",
            ".css": "CSS",
            ".json": "JSON",
            ".xml": "XML",
            ".md": "Markdown",
            ".sh": "Shell",
            ".bat": "Batch"
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

                extension = full_path.suffix.lower()

                language = language_map.get(
                    extension,
                    "Unknown"
                )

                try:

                    content = full_path.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )

                except Exception:
                    continue

                line_count = len(content.splitlines())

                sha = hashlib.sha256(
                    content.encode("utf-8")
                ).hexdigest()

                index["files"][relative] = {
                    "language": language,
                    "extension": extension,
                    "lines": line_count,
                    "size": len(content),
                    "hash": sha
                }

                index["summary"]["total_files"] += 1
                index["summary"]["total_lines"] += line_count

                langs = index["summary"]["languages"]

                langs[language] = langs.get(language, 0) + 1

        return index

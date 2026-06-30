import json


class ContextKernel:

    def __init__(self, memory, code_memory):

        self.memory = memory
        self.code_memory = code_memory

    # -----------------------------
    # MAIN CONTEXT BUILDER
    # -----------------------------
    def build_context(self, project, task, max_files=6):

        # 1. Load structured memory (NOT raw logs)
        project_memory = self.memory._read_json(
            self.memory._project_path(project) + "/knowledge.json"
        )

        # 2. Extract intent keywords
        keywords = self._extract_keywords(task, project_memory)

        # 3. Retrieve relevant code (RAG)
        retrieved_code = self.code_memory.retrieve_relevant_files(
            keywords,
            limit=max_files
        )

        # 4. Compress memory (VERY IMPORTANT)
        compressed_memory = self._compress_memory(project_memory)

        return {
            "memory": compressed_memory,
            "retrieved_code": retrieved_code,
            "keywords": keywords
        }

    # -----------------------------
    # SIMPLE COMPRESSION (can be upgraded later)
    # -----------------------------
    def _compress_memory(self, memory):

        if not memory:
            return {}

        return {
            "summary_keys": list(memory.keys())[:20],
            "important_values": {
                k: str(v)[:300]
                for k, v in memory.items()
            }
        }

    # -----------------------------
    # KEYWORD EXTRACTION
    # -----------------------------
    def _extract_keywords(self, task, memory):

        words = []

        if isinstance(task, dict):
            words += list(task.keys())
            words += str(task.get("module", "")).split()

        words += list(memory.keys())

        return list(set([w.lower() for w in words if isinstance(w, str)]))

import os


class CodeMemory:

    def __init__(self):
        self.workspace = "workspace"

    def retrieve_relevant_files(self, query_keywords):

        matches = []

        for root, _, files in os.walk(self.workspace):

            for f in files:

                path = os.path.join(root, f)

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                except:
                    continue

                score = self._score(content, query_keywords)

                if score > 0:
                    matches.append({
                        "file": path,
                        "score": score,
                        "snippet": content[:1000]
                    })

        matches.sort(key=lambda x: x["score"], reverse=True)

        return matches[:5]

    def _score(self, content, keywords):

        content_lower = content.lower()

        score = 0

        for k in keywords:
            if k.lower() in content_lower:
                score += 1

        return score

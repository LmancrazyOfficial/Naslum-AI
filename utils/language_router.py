def detect_language(file_path: str):
    if file_path.endswith(".py"):
        return "python"
    if file_path.endswith(".js"):
        return "node"
    if file_path.endswith(".cpp"):
        return "cpp"
    return "unknown"

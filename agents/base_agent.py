class BaseAgent:

    def __init__(self, name, llm, tools, memory):
        self.name = name
        self.llm = llm
        self.tools = tools
        self.memory = memory

    def can_handle(self, task):
        return False

    def execute(self, task):
        raise NotImplementedError

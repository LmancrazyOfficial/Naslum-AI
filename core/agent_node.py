import threading


class AgentNode:

    def __init__(self, agent):

        self.agent = agent
        self.lock = threading.Lock()

    def run_task(self, task):

        with self.lock:
            return self.agent.execute(task)

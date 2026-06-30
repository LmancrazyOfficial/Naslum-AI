from core.agent_node import AgentNode
from core.task import Task


class SwarmCoordinator:

    def __init__(self, agents):

        self.nodes = [AgentNode(a) for a in agents]

    def distribute(self, tasks):

        results = []

        for i, task in enumerate(tasks):

            node = self.nodes[i % len(self.nodes)]

            result = node.run_task(task)

            results.append(result)

        return results

import logging
from collections import deque

import networkx as nx

from .basesolver import BaseSolver
from .lp import LP

LOGGER = logging.getLogger(__name__)


def connected_components(graph: nx.DiGraph):
    seen = set()
    for root in graph:
        if root not in seen:
            seen.add(root)
            sg, dq = [], deque([root])
            while dq:
                node = dq.popleft()
                sg.append(node)
                for n in graph.neighbors(node):
                    if n not in seen:
                        seen.add(n)
                        dq.append(n)
            yield sg


class Disjoint(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)

    @staticmethod
    def create_graph(clients, ingredients):
        G = nx.DiGraph()
        i_LUT: dict = {i: idx for i, idx in zip(ingredients, range(len(ingredients)))}
        for c in clients:
            for i in c.likes | c.dislikes:
                G.add_edge(f"c{c.id}", f"i{i_LUT[i]}", capacity=1.0)
                G.add_edge(f"i{i_LUT[i]}", f"c{c.id}", capacity=1.0)
        return G

    def disjoint_sets(self, data):
        components = list(connected_components(self.create_graph(*data)))
        components = [list(map(lambda s: int(s[1:]), filter(lambda t: t[0] == 'c', component))) for component in components]
        LOGGER.info(f"Found {len(components)} disjoint problem sets.")

        return [
            (
                [data[0][c] for c in cc],
                sorted(set([i for c in cc for i in data[0][c].likes | data[0][c].dislikes]))
            )
            for cc in components
        ]

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        problem_sets = self.disjoint_sets(self.data)
        self.solution = set()
        for data in problem_sets:
            # create graph for max flow / min cut
            G: nx.DiGraph = self.create_graph(*data)
            # remove i-nodes
            for n in list(nt for nt in G.nodes if nt.startswith('i')):
                for ie in G.in_edges(n):
                    for oe in G.edges(n):
                        fn, tn = ie[0], oe[1]
                        if fn != tn:
                            G.add_edge(fn, tn, capacity=1.0)
                G.remove_node(n)
            # add source and target node
            for n in list(G.nodes):
                G.add_edge("source", n, capacity=1.0)
                G.add_edge(n, "target", capacity=1.0)

            cut_value, partition = nx.minimum_cut(G, "source", "target")

            lp = LP()
            lp.data = data
            if lp.solve():
                self.solution.update(set(lp.solution))

        return True

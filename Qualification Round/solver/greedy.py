import logging
from typing import List

from .basesolver import BaseSolver
from .project import Project
from .contributor import Contributor

LOGGER = logging.getLogger(__name__)


class Greedy(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str=None):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        contributors: List[Contributor] = self.data[0]
        projects: List[Project] = self.data[1]
        all_skills = set.union(*[set(c.skills.keys()) for c in contributors] + [set(p.roles.keys()) for p in projects])
        max_levels = {s: max([c.skills[s] if s in c.skills else 0 for c in contributors]) for s in all_skills}
        LOGGER.info(f"Overall {len(all_skills)} skills/roles.")
        for p in projects:
            p.util = p.score / p.duration
            p.viable = all([max_levels[r] >= p.roles[r] for r in p.roles])
        viable_p = len([p for p in projects if p.viable])
        return False

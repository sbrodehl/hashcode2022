import logging
import random

from .basesolver import BaseSolver

LOGGER = logging.getLogger(__name__)


class Random(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str=None):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        while len(self.solution) == 0:
            self.solution = [i for i in self.data[1] if random.randint(0, 1) > 0]

        return True

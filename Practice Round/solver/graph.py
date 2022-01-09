import logging

import numpy as np
import matplotlib.pyplot as plt

from .basesolver import BaseSolver

LOGGER = logging.getLogger(__name__)


class Graph(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str=None):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        C = len(self.data[0])
        I = len(self.data[1])
        ingredients = {i: idx for i, idx in zip(self.data[1], range(I))}

        likes = np.zeros(I, dtype=np.uint16 if C < 65535 else np.uint32)
        dislikes = np.zeros(I, dtype=np.uint16 if C < 65535 else np.uint32)

        for c in self.data[0]:
            for i in c.likes:
                likes[ingredients[i]] += 1
            for i in c.dislikes:
                dislikes[ingredients[i]] += 1

        fig, ax = plt.subplots(figsize=(15, 5), dpi=300)
        ind = np.arange(I)

        likes = likes.astype(np.float) / C
        dislikes = dislikes.astype(np.float) / C

        ax.margins(x=0)
        ax.bar(ind, likes, label='Likes')
        ax.bar(ind, -1 * dislikes, label='Dislikes')

        ax.axhline(0, color='grey', linewidth=0.8)
        ax.set_ylabel('Dis-/Likes [% of clients]')
        ax.set_title('Dis- / Likes by Ingredients (in %)')
        ax.legend()

        plt.tight_layout()
        plt.show()

        return False

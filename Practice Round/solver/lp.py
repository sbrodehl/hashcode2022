import logging

import numpy as np

import gurobipy as gp
from gurobipy import GRB

from .basesolver import BaseSolver

LOGGER = logging.getLogger(__name__)


class LP(BaseSolver):
    """Solve the problem nice and steady!
    """
    def __init__(self, input_str):
        super().__init__(input_str)

    def solve(self):
        """Compute a solution to the given problem.

        Save everything in an internal state.

        :return: True, if a solution is found, False otherwise
        """
        C = len(self.data[0])
        I = len(self.data[1])
        ingredients = {i: idx for i, idx in zip(self.data[1], range(I))}

        constraints = 0
        for c in self.data[0]:
            if len(c.likes) > 0:
                constraints += 1
            if len(c.dislikes) > 0:
                constraints += 1

        try:
            # Create a new model
            m = gp.Model("one-pizza")

            x = m.addMVar(shape=tuple([I]), vtype=GRB.BINARY, name="pizza")

            # Set objective
            m.setObjective(..., GRB.MAXIMIZE)

            # add constraints
            ...

            # Optimize model
            m.optimize()

            for v in m.getVars():
                print('%s %g' % (v.varName, v.x))

            print('Obj: %g' % m.objVal)

        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))
            return False

        except AttributeError:
            print('Encountered an attribute error')
            return False

        return True

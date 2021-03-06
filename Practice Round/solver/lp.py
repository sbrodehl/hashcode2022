import logging

import gurobipy as gp
from gurobipy import GRB

from .basesolver import BaseSolver

LOGGER = logging.getLogger(__name__)
logging.getLogger("gurobipy").setLevel(logging.ERROR)  # prevent duplicate gurobi output to console


class LP(BaseSolver):
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

        try:
            # Create a new model
            m = gp.Model("one-pizza")
            var_c = m.addVars(C, vtype=GRB.BINARY, name='c')
            var_i = m.addVars(I, vtype=GRB.BINARY, name='i')

            # Set objective
            score = var_c.sum()
            m.setObjective(score, GRB.MAXIMIZE)

            # add constraints
            for v, client in zip(var_c.values(), self.data[0]):
                m.addConstrs(v <=     var_i[ingredients[i]] for i in client.likes   )
                m.addConstrs(v <= 1 - var_i[ingredients[i]] for i in client.dislikes)

            # Optimize model
            m.setParam(GRB.Param.MIPGap, 0)  # try to solve optimally
            m.optimize()

            print('Obj: %g' % m.objVal)
            
            self.solution = [self.data[1][i] for i, v in var_i.items() if v.x]
            
        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))
            return False

        except AttributeError:
            print('Encountered an attribute error')
            return False

        return True

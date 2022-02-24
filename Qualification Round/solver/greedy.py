import logging
from typing import List

from .basesolver import BaseSolver
from .project import Project
from .contributor import Contributor

from tqdm import tqdm

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
        self.solution = []
        contributors: List[Contributor] = self.data[0]
        projects: List[Project] = self.data[1]
        all_skills = set.union(*[set(c.skills.keys()) for c in contributors] + [set([x[0] for x in p.roles]) for p in projects])

        LOGGER.info(f"Overall {len(all_skills)} skills/roles.")
        steps = set([0])
        total_score = 0
        tq = tqdm(total=len(projects))
        while len(steps) > 0:
            step = min(steps)
            steps.remove(step)

            for c in contributors:
                c.stupidity = - sum(c.skills.values())
            contributors = sorted(contributors, key=lambda c: c.stupidity, reverse=True)
            max_levels = {s: max([c.skills[s] if s in c.skills else 0 for c in contributors]) for s in all_skills}

            for p in projects:
                if p.scheduled:
                    continue
                p.remaining_time = p.best_before - step - p.duration
                p.possible_score = (p.score - max(0, (- p.remaining_time)))
                p.util = p.possible_score / (p.duration + max(0, p.remaining_time))

                p.viable = all([max_levels[r] >= p.roles_dict[r] for r in p.roles_dict])

            possible_score = 0
            for p in sorted([p for p in projects if p.viable and not p.scheduled], key=lambda p: p.util, reverse=True):
                p.team = []
                assigned = set()

                # assign contributors
                for r, rl in p.roles:
                    for c in contributors:
                        if c.id in assigned:
                            continue
                        if c.free_from <= step and (c.skills[r] >= rl or (c.skills[r] == rl - 1 and any([_c.skills[r] >= rl for (_, _c) in p.team]))):
                            assigned.add(c.id)
                            p.team.append((r, c))
                            break
                    else:
                        p.team = []
                        possible_score += p.possible_score
                        break
                else:
                    # project doable
                    total_score += p.possible_score
                    p.scheduled = True
                    self.solution.append(p)
                    tq.update()
                    # check level up
                    assert len(p.roles) == len(p.team)
                    for idx, (r, c) in enumerate(p.team):
                        c.free_from = step + p.duration
                        if c.skills[r] <= p.roles[idx][1]:
                            c.skills[r] += 1
                    steps.add(step + p.duration)
            if possible_score == 0:
                break
        return True

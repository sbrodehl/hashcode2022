from typing import List, Dict, Set
import time
import logging
from collections import deque

from .project import Project
from .contributor import Contributor


LOGGER = logging.getLogger(__name__)


class Simulation:

    def __init__(self, projects: List[Project], contributors: List[Contributor]):
        self.step: int = -1
        self.projects: List[Project] = projects
        self.contributors: List[Contributor] = contributors
        self.schedule: deque[Project] = deque()
        self.teams: dict[str, List[str]] = {}
        self.done: List[Project] = []
        self.waiting: List[int] = []
        self._del_proj: Set[str] = set()
        self._proj_lut = {p.name: pid for pid, p in enumerate(self.projects)}
        self._cons_lut = {c.name: cid for cid, c in enumerate(self.contributors)}
        self.learning: int = 0
        self.mentoring: int = 0
        self._timer = time.CLOCK_THREAD_CPUTIME_ID

    def setup(self, schedule):
        self.schedule = deque([p_n for p_n, _ in schedule])
        self.teams = {p_n: p_c for p_n, p_c in schedule}
        return self

    def run(self, duration: int = None):
        start = time.clock_gettime(self._timer)

        # run steps of the simulation
        while len(self.schedule) > 0:
            self.step += 1
            if duration is not None and self.step > duration:
                break
            self.tick()
            # check if contributors are still busy, projects are getting done
            if len(self._del_proj) == 0 and not self.contributors_busy():
                # none is busy, but no proj done ... the rest is not doable
                break
            self.update_projects()
        LOGGER.info(
            f"{self.__class__.__name__}::run "
            f"{time.clock_gettime(self._timer) - start:.5f}s"
        )
        return self

    def contributors_busy(self):
        return any(c.free_from > self.step for c in self.contributors)

    def update_projects(self):
        for p_name in self._del_proj:
            self.schedule.remove(p_name)
        self._del_proj.clear()

    def tick(self):
        for p in self.schedule:
            p = self.projects[self._proj_lut[p]]
            c = [self.contributors[self._cons_lut[c_n]] for c_n in self.teams[p.name]]
            assert len(p.roles) == len(c), f"Invalid submission: The number of listed contributors for project {p.name} is {len(c)} instead of {len(p.roles)}."
            # check if contributors are available and skill levels match
            if all([rc.free_from <= self.step and (rc.skills[r] >= rl or (rc.skills[r] == rl - 1 and any(self.contributors[self._cons_lut[tc]].skills[r] >= rl for tc in self.teams[p.name]))) for (r, rl), rc in zip(p.roles, c)]):
                # set contributors unavailable and increase skill levels
                for (r, rl), rc in zip(p.roles, c):
                    self.waiting.append(self.step - rc.free_from)
                    rc.free_from = self.step + p.duration
                    if rc.skills[r] == rl - 1:
                        self.mentoring += 1
                    if rc.skills[r] <= rl:
                        rc.skills[r] += 1
                        self.learning += 1
                p.scheduled = True
                p.remaining_time = p.best_before - self.step - p.duration
                p.points = max(0, (p.score - max(0, -p.remaining_time)))
                self.done.append(p)
                self._del_proj.add(p.name)

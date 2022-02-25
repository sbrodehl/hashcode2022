#!/usr/bin/env python3
import logging
from dataclasses import dataclass, field

from .parsing import parse_input, parse_output
from .simulation import Simulation

LOGGER = logging.getLogger(__name__)


class Markup:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


@dataclass
class Score:
    scores: list = field(default_factory=list)
    total: int = 0
    insights: dict = field(default_factory=dict)

    def add(self, other):
        self.scores.append(other)
        self.total += other

    def print_insights(self):
        nsghs = self.insights
        LOGGER.info(f"Submission: {Markup.BOLD}Scoring & Insights{Markup.END}")
        LOGGER.info(f"Your submission scored {Markup.BOLD}{self.total:,} points{Markup.END}.")

        completed_projects_pct = 100. * nsghs['completed'] / nsghs['all']
        _str = f" - projects {Markup.BOLD}completed{Markup.END}: {nsghs['completed']} ({Markup.BOLD}{completed_projects_pct:.2f}%{Markup.END} of all projects)."
        LOGGER.info(_str)

        best_before_pct = 100. * nsghs['full_points'] / nsghs['all']
        _str = f" - projects completed before their 'best before' time in days ({Markup.BOLD}scoring full points{Markup.END}): {nsghs['full_points']} ({Markup.BOLD}{best_before_pct:.2f}%{Markup.END} of all projects)"
        LOGGER.info(_str)

        zer_pnt_pct = 100. * nsghs['zero_points'] / nsghs['all']
        _str = f" - projects completed but {Markup.BOLD}scoring 0 points{Markup.END} (because they were completed too long after their 'best before' time): {nsghs['zero_points']} ({Markup.BOLD}{zer_pnt_pct:.2f}%{Markup.END} of all projects)"
        LOGGER.info(_str)

        LOGGER.info(f" - number of times a contributor got {Markup.BOLD}mentored{Markup.END} on a project: {Markup.BOLD}{nsghs['mentoring_points']}{Markup.END}")
        LOGGER.info(f" - number of times a contributor {Markup.BOLD}increased{Markup.END} their {Markup.BOLD}skill level{Markup.END} thanks to completing a project: {Markup.BOLD}{nsghs['learning_points']}{Markup.END}")

        LOGGER.info(f" - contributors were {Markup.BOLD}waiting{Markup.END} for their next project to start {Markup.BOLD}{nsghs['waiting']:.2f} days{Markup.END} on average")
        bored_pct = 100. * (nsghs['all_contributors'] - nsghs['bored_contributors']) / nsghs['all_contributors']
        LOGGER.info(f" - {nsghs['all_contributors'] - nsghs['bored_contributors']} contributors out of {nsghs['all_contributors']} worked on {Markup.BOLD}at least one project{Markup.END} ({Markup.BOLD}{bored_pct:.2f}%{Markup.END})")


def set_log_level(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def compute_score(file_in, file_out):
    """
    Compute score (with bonus) of submission
    :param file_in: input file
    :param file_out: output file (solution)
    :return: Score
    """
    # read input and output files
    contributors, projects = parse_input(file_in)
    solution = parse_output(file_out)
    s = Score()
    sim = Simulation(projects, contributors)
    sim.setup(solution).run()
    # add some insights
    s.insights["waiting"] = 1. * sum(sim.waiting) / len(sim.waiting)
    s.insights["completed"] = len(sim.done)
    s.insights["all"] = len(projects)
    s.insights["full_points"] = 0
    s.insights["zero_points"] = 0
    s.insights["all_contributors"] = len(contributors)
    s.insights["bored_contributors"] = 0
    s.insights["learning_points"] = sim.learning
    s.insights["mentoring_points"] = sim.mentoring
    for d_p in sim.done:
        s.add(d_p.points)
        if d_p.points == d_p.score:
            s.insights["full_points"] += 1
        if d_p.points == 0:
            s.insights["zero_points"] += 1
    for c in sim.contributors:
        if c.free_from == 0:
            s.insights["bored_contributors"] += 1
    return s

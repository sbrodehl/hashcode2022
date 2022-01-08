#!/usr/bin/env python3
import logging
from dataclasses import dataclass, field

from .parsing import parse_input, parse_output

LOGGER = logging.getLogger(__name__)


@dataclass
class Score:
    scores: list = field(default_factory=list)
    total: int = 0

    def add(self, other):
        self.scores.append(other)
        self.total += other


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
    problem_set = parse_input(file_in)
    solution = parse_output(file_out)
    s = Score()
    for client in problem_set[0]:
        # check if all likable ingredients are in,
        # and none of the disliked ones
        if client.likes.issubset(solution) and client.dislikes.isdisjoint(solution):
            s.add(1)

    return s


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='print score', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file_in', type=str, help='input file e.g. a_example.in')
    parser.add_argument('file_out', type=str, help='output file e.g. a_example.out')
    parser.add_argument('--debug', action='store_true', help='set debug level')
    args = parser.parse_args()

    set_log_level(args)

    score = compute_score(args.file_in, args.file_out)

    print("Score for {}: {} points".format(args.file_out, score.total))

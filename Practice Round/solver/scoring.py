#!/usr/bin/env python3
import logging
from dataclasses import dataclass, field

from .parsing import parse_input, parse_output

LOGGER = logging.getLogger(__name__)


@dataclass
class Score:
    scores: list = field(default_factory=list)
    total: int = 0

    def add(self, diff_ingredients_sq):
        pass

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
    return 0


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

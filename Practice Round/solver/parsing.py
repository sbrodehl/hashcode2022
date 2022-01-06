import logging
import collections

from .pizza import Pizza
from .delivery import Delivery

LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: None
    """
    LOGGER.info("Parsing file '{}'".format(file_in))

    with open(file_in, 'r') as f:
        first_line = f.readline().strip()

    LOGGER.info("Parsing '{}' - Done!".format(file_in))

    return None


def parse_output(file_out, problem_set):
    """
    Parse output file
    :param file_out: output file name (solution)
    :param problem_set: input problem set
    :return: None
    """
    LOGGER.info("Parsing '{}'".format(file_out))
    
    with open(file_out, 'r') as f:
        first_line = f.readline().strip()

    LOGGER.info("Parsing '{}' - Done!".format(file_out))

    return None


def write_output(file_out, solution):
    LOGGER.debug("Writing solution '{}'".format(file_out))
    with open(file_out, 'w') as f:
        f.write(f"{solution}")

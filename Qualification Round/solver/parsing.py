import logging

from .contributor import Contributor
from .project import Project

LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: None
    """
    LOGGER.info("Parsing file '{}'".format(file_in))

    contributors = []
    projects = []

    with open(file_in, 'r') as f:
        c, p = map(int, f.readline().strip().split(" "))
        for cidx in range(c):
            c_name, c_skills = list(f.readline().strip().split(" "))
            c_skills_l = {}
            for sidx in range(int(c_skills)):
                s_name, s_level = list(f.readline().strip().split(" "))
                c_skills_l[s_name] = int(s_level)
            contributors.append(Contributor(cidx, c_name, c_skills_l))
        for pidx in range(p):
            p_name, p_d, p_s, p_b, p_r = list(f.readline().strip().split(" "))
            p_roles = {}
            for ridx in range(int(p_r)):
                r_x, r_l = list(f.readline().strip().split(" "))
                p_roles[r_x] = int(r_l)
            projects.append(Project(pidx, p_name, p_d, p_s, p_b, p_roles))

    LOGGER.info("Parsing '{}' - Done!".format(file_in))
    LOGGER.info(f"Found {c} contributors and {len(projects)} projects.")

    return contributors, projects


def parse_output(file_out):
    """
    Parse output file
    :param file_out: output file name (solution)
    :return: None
    """
    LOGGER.info("Parsing '{}'".format(file_out))
    
    with open(file_out, 'r') as f:
        ingredients = f.readline().strip().split(" ")
        i = int(ingredients[0])
        ingredients = ingredients[1:]
        assert len(ingredients) == i

    LOGGER.info("Parsing '{}' - Done!".format(file_out))
    return set(ingredients)


def write_output(file_out, solution):
    LOGGER.debug("Writing solution '{}'".format(file_out))
    with open(file_out, 'w') as f:
        f.write(f"{str(len(solution))} {' '.join(sorted(solution))}\n")

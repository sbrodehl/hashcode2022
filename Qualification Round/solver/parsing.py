import logging
from collections import defaultdict

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
            c_skills_l = defaultdict(lambda: 0)
            for sidx in range(int(c_skills)):
                s_name, s_level = list(f.readline().strip().split(" "))
                c_skills_l[s_name] = int(s_level)
            contributors.append(Contributor(cidx, c_name, c_skills_l, 0))
        for pidx in range(p):
            p_name, p_d, p_s, p_b, p_r = list(f.readline().strip().split(" "))
            p_roles = []
            p_roles_d = {}
            for ridx in range(int(p_r)):
                r_x, r_l = list(f.readline().strip().split(" "))
                p_roles.append((r_x, int(r_l)))
                p_roles_d[r_x] = max(int(r_l), p_roles_d[r_x] if r_x in p_roles_d else 0)
            projects.append(Project(pidx, p_name, int(p_d), int(p_s), int(p_b), p_roles, p_roles_d, False))

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
    solution = []
    with open(file_out, 'r') as f:
        p = int(f.readline().strip())
        for pid in range(p):
            p_name = f.readline().strip()
            team = f.readline().strip().split(" ")
            solution.append((p_name, team))

    LOGGER.info("Parsing '{}' - Done!".format(file_out))
    return solution


def write_output(file_out, solution):
    LOGGER.debug("Writing solution '{}'".format(file_out))
    with open(file_out, 'w') as f:
        f.write(f"{str(len(solution))}\n")
        for p in solution:
            f.write(f"{str(p.name)}\n")
            f.write(f"{' '.join([t[1].name for t in p.team])}\n")

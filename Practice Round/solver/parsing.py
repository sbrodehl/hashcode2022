import logging

from .client import Client

LOGGER = logging.getLogger(__name__)


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: None
    """
    LOGGER.info("Parsing file '{}'".format(file_in))

    clients = []
    ingredients = set()

    with open(file_in, 'r') as f:
        C = int(f.readline().strip())
        for cid in range(C):
            likes = list(f.readline().strip().split(" "))
            L = int(likes[0])
            likes = set(likes[1:])
            assert len(likes) == L
            dislikes = list(f.readline().strip().split(" "))
            D = int(dislikes[0])
            dislikes = set(dislikes[1:])
            assert len(dislikes) == D
            assert set(likes).isdisjoint(set(dislikes))
            clients.append(Client(cid, likes, dislikes))
            ingredients.update(likes)
            ingredients.update(dislikes)

    # sort and cast to list
    ingredients = list(sorted(ingredients))

    LOGGER.info("Parsing '{}' - Done!".format(file_in))
    LOGGER.info(f"Found {C} clients (pizzas) with overall {len(ingredients)} different ingredients.")

    return clients, ingredients


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

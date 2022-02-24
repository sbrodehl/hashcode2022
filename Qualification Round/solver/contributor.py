from dataclasses import dataclass


@dataclass
class Contributor:
    """Class representing a contributor with id, name and skills."""
    id: int
    name: str
    skills: dict
    free_from: int

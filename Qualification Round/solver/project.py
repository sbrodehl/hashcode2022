from dataclasses import dataclass


@dataclass
class Project:
    """Class representing a project with attributes."""
    id: int
    name: str
    duration: int
    score: int
    best_before: int
    roles: dict

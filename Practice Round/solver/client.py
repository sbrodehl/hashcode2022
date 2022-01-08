from dataclasses import dataclass


@dataclass
class Client:
    """Class representing a pizza with ingredients."""
    id: int
    likes: set
    dislikes: set

from .parsing import parse_input, write_output
from .scoring import compute_score


class BaseSolver(object):
    """Don't touch this!
    This class makes sure that those two methods gets implemented,
    as needed in main.py.
    """

    def __init__(self, input_str=None):
        """Initialisation of the given problem.
        """
        self.input_str = input_str
        self.data = parse_input(self.input_str) if input_str is not None else None
        self.solution = []

    def solve(self):
        """Solves the problem and stores the solution internally.

        :return: True, if a solution is found, False otherwise
        """
        raise NotImplementedError("This method needs to be implemented.")

    def write(self, output_str):
        write_output(output_str, self.solution)
        s = compute_score(self.input_str, output_str)
        s.print_insights()

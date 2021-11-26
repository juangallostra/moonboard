from typing import Any, List
from adapters.base_adapter import BaseProblemAdapter
from models.problem import Problem, Move

class CRGProblemAdapter(BaseProblemAdapter):
    """
    Map problem data to a Python object that the renderer can use.
    """
    def map_problem(self, problem_data: List[Any]) -> Problem:
        """
        Given a problem data dictionary, return a Problem object

        :param problem_data: Source from which to map the problem
        :type problem_data: dict
        :return: Problem object with the parsed problem data as attributes
        :rtype: Problem
        """
        # Make copy of problem data so we don't modify the original.
        # Problem data is the first item in the list
        # [[5, 5, "s"], [4, 5, "s"], [7, 7, "m"], [9, 8, "m"], [8, 12, "m"], [6, 16, "m"], [10, 16, "m"], [5, 17, "f"]]
        problem_data_copy = problem_data[0].copy()
        # Parse moves
        # [5, 5, "s"]
        moves = []
        for move_idx in range(len(problem_data_copy)):
            id = move_idx + 1
            # row mapping and col mapping -> zero based
            col = problem_data_copy[move_idx][0]
            row = problem_data_copy[move_idx][1] + 1
            is_start = problem_data_copy[move_idx][2] == "s"
            is_end = problem_data_copy[move_idx][2] == "f"
            m = Move(id, row, col, str(row) + ' ' + str(col), is_start, is_end)
            moves.append(m)
        # Parse rest of data
        return Problem(
            "",
            "",
            moves,
            False)

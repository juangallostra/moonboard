from typing import List
from adapters.base_adapter import BaseProblemAdapter
from models.problem import Move, Problem

class AhoughtonAdapter(BaseProblemAdapter):
    def map_problem(self, problem_data: List[str]) -> Problem:
        """
        Given a problem obtained from the Ahoughton generator, return a Problem object

        :param problem_data: Source from which to map the problem
        :type problem_data: List[str]
        :return: Problem object with the parsed problem data as attributes
        :rtype: Problem
        """
        # Make copy of problem data so we don't modify the original.
        # Problem data is in the format:
        # ['D18', 'G13', ...]
        problem_data_copy = problem_data.copy()
        # Parse moves
        # 'D18'
        moves = []
        for move_idx in range(len(problem_data_copy)):
            id = move_idx + 1
            # row mapping and col mapping -> zero based
            col = ord(problem_data_copy[move_idx][0].lower()) - ord('a')
            row = int(problem_data_copy[move_idx][1:])
            is_start = row <= 6
            is_end = row == 18
            m = Move(id, row, col, str(row) + ' ' + str(col), is_start, is_end)
            moves.append(m)
        # Parse rest of data
        return Problem(
            '',
            '',
            moves,
            False
        )
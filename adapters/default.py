from typing import Any, Dict
from adapters.base_adapter import BaseProblemAdapter
from models.problem import Problem, Setter, Move

class DefaultProblemAdapter(BaseProblemAdapter):
    """
    Map problem data to a Python object that the renderer can use.
    """
    def map_problem(self, problem_data: Dict[str, Any]) -> Problem:
        """
        Given a problem data dictionary, return a Problem object

        :param problem_data: Source from which to map the problem
        :type problem_data: dict
        :return: Problem object with the parsed problem data as attributes
        :rtype: Problem
        """
        # Make copy of problem data so we don't modify the original
        problem_data_copy = problem_data.copy()
        # Parse setter
        firstname = problem_data_copy['Setter'].pop('Firstname')
        lastname = problem_data_copy['Setter'].pop('Lastname')
        nickname = problem_data_copy['Setter'].pop('Nickname')
        setter = Setter(nickname, firstname, lastname)
        problem_data_copy['setter'] = setter
        # Parse moves
        #  {
        #      "Id": 1910061,
        #      "Description": "J4",
        #      "IsStart": false,
        #      "IsEnd": false
        #   }
        moves = []
        for move in problem_data_copy.pop('Moves'):
            id = move['Id']
            if isinstance(id, str):
                id = int(id)
            # row mapping
            col = move['Description'][0]
            row = move['Description'][1:] 
            move_col = ord(col.lower()) - ord('a')
            move_row = row
            if isinstance(row, str):
                move_row = int(row)
            m = Move(id, move_row, move_col, move['Description'], move['IsStart'], move['IsEnd'])
            moves.append(m)
        # Parse rest of data
        return Problem(
            problem_data_copy.pop('Name'),
            problem_data_copy.pop('Grade'),
            moves,
            problem_data_copy.pop('IsBenchmark'),
            **problem_data_copy)

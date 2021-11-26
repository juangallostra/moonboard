from models.problem import Problem


class BaseProblemAdapter():
    """
    Map problem data to a Python object that the renderer can use.
    """

    def map_problem(self, problem_data) -> Problem:
        """
        Given the raw data of a problem, convert it to a Problem object and return it.
        
        :param problem_data: Source from which to map the problem
        :type problem_data: dict
        :return: Problem object with the parsed problem data as attributes
        :rtype: Problem
        :raises NotImplementedError: If the method is not implemented 
        """
        raise NotImplementedError

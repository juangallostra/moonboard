from models.problem import Move, Problem, Setter



class BaseProblemAdapter():
    """
    Map problem data to a Python object that the renderer can use.
    """

    def map_problem(self, problem_data) -> Problem:
        raise NotImplementedError


class DefaultProblemAdapter(BaseProblemAdapter):
    """
    Map problem data to a Python object that the renderer can use.
    """
    def map_problem(self, problem_data: dict) -> Problem:
        """
        Given a problem data dictionary, return a Problem object

        Args:
            problem_data (dict): Source from which to map the problem.

        Returns:
            Problem: Problem object with the parsed problem data as attributes
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


class MoonBoard():
    """
    Class that encapsulates Moonboard layout info for a specific year
    """

    def __init__(self, year_layout: int, image: str, rows: int = 18, cols: int = 11) -> None:
        """
        Initialize a MoonBoard object.

        Args:
            year_layout (int): Year from which to obtain the Moonboard layout.
            image (str): path to the moonboard  layout image.
            rows (int, optional): Number of rows of the board. Defaults to 18.
            cols (int, optional): Number of rows of the board. Defaults to 11.
        """
        self._year_layout = year_layout
        self._image = image
        self._rows = rows
        self._cols = cols

    def get_rows(self) -> int:
        """Get number of rows of the board

        Returns:
            int: Number of rows of the board
        """
        return self._rows

    def get_cols(self) -> int:
        """Get number of columns of the board

        Returns:
            int: Number of columns of the board
        """
        return self._cols

    def get_year_layout(self) -> int:
        """Get the year in which this board layout was published

        Returns:
            int: year in which this board layout was published
        """
        return self._year_layout

    def get_image(self) -> str:
        """Get the path to the image file for this board layout

        Returns:
            str: image path
        """
        return self._image


def get_moonboard(year: int) -> MoonBoard:
    """
    Given a year, return a Moonboard object encapsulating the
    Moonboard layout info of that year.

    Args:
        year (int): Year of the desired Moonboard layout.

    Raises:
        ValueError: Year is not a valid Moonboard year.

    Returns:
        Moonboard: Moonboard object encapsulating the Moonboard layout info.
    """
    if year == 2016:
        return MoonBoard(2016, 'moonboards/2016.jpg')
    elif year == 2017:
        return MoonBoard(2017, 'moonboards/2017.jpg')
    elif year == 2019:
        return MoonBoard(2019, 'moonboards/2019.jpg')
    elif year == 2020:
        return MoonBoard(2020, 'moonboards/2020.jpg', rows=12)
    raise ValueError('Invalid year')


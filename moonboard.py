

class MoonBoard():
    """
    Class that encapsulates Moonboard layout info for a specific year.

    :param year_layout: Year in which this board layout was published
    :type year_layout: int
    :param image: Path to the image file for this board layout
    :type image: str
    :param rows: Number of rows of the board. Defaults to 18
    :type rows: int, optional
    :param cols: Number of columns of the board. Defaults to 11
    :type cols: int, optional
    """

    def __init__(self, year_layout: int, image: str, rows: int = 18, cols: int = 11) -> None:
        """
        Initialize a MoonBoard object.
        """
        self._year_layout = year_layout
        self._image = image
        self._rows = rows
        self._cols = cols

    def __str__(self) -> str:
        """Get a user friendly string representation of the MoonBoard class

        :return: User firendly string representation if this Moonboard object
        :rtype: str
        """
        return f"{__class__.__name__} for {self._moonboard.get_year_layout()} layout"

    def __hash__(self) -> int:
        """
        Compute hash from the year,  image path
        """
        return hash(self._year_layout) ^ hash(self._image) ^ hash(self._rows) ^ hash(self._cols)

    def __eq__(self, __o: object) -> bool:
        """
        Test for equality between two MoonBoard objects
        """
        if hash(self) != hash(__o):  # if hashes are not equal, objects cannot be equal
            return False
        return self._year_layout == __o._year_layout and self._image == __o._image and self._rows == __o._rows and self._cols == __o._cols

    def get_rows(self) -> int:
        """
        Get number of rows of the board

        :return: Number of rows of the board
        :rtype: int 
        """
        return self._rows

    def get_cols(self) -> int:
        """
        Get number of columns of the board

        :return: Number of columns of the board
        :rtype: int
        """
        return self._cols

    def get_year_layout(self) -> int:
        """
        Get the year in which this board layout was published

        :return: Year in which this board layout was published
        :rtype: int 
        """
        return self._year_layout

    def get_image(self) -> str:
        """
        Get the path to the image file for this board layout

        :return: Image path
        :rtype: str 
        """
        return self._image


def get_moonboard(year: int) -> MoonBoard:
    """
    Factory function. Given a year, return a Moonboard object encapsulating the
    Moonboard layout info of that year.

    :param year: Year of the desired Moonboard layout
    :type year: int
    :return: Moonboard object encapsulating the Moonboard layout info
    :rtype: MoonBoard
    :raises ValueError: Year is not a valid Moonboard year
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

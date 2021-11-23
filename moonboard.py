from typing import Tuple, Dict
from PIL import Image, ImageDraw, ImageFont
import json
from dataclasses import dataclass, field


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


@dataclass
class RendererConfig:
    """
    Class for keeping the configuration parameters of the renderer
    Default values are set for the following board layouts: 2016, 2017, 2019
    """
    # colors for different type of holds
    _color_map: Dict[str, Tuple[int, int, int]] = field(default_factory=lambda: {
        'start': (0, 255, 0),  # green
        'middle': (0, 0, 255),  # blue
        'top': (255, 0, 0)  # red
    })
    # geometry of board images
    _bbox_side: float = 51.5
    _offset_x: float = 70
    _offset_y: float = 60
    _circle_width: float = 7
    # text configuration for rendering problem name
    _text_size: int = 30
    _text_position: Tuple[float, float] = (15, 980)
    _text_color: Tuple[int, int, int] = (255, 255, 255)
    _font: str = "fonts/MilkyNice.ttf"


class ProblemRenderer():
    """
    Generic class to render a problem on a board
    """

    def __init__(self, moonboard_layout: MoonBoard, render_config: RendererConfig) -> None:
        """
        Initialize a ProblemRenderer object.

        Args:
            moonboard_layout (MoonBoard): Layout of the Moonboard to render on.
            render_config (RendererConfig): Config for rendering Moonboard Problems
        """
        self._moonboard = moonboard_layout
        self._render_config = render_config

    def __str__(self) -> str:
        return f"{__class__.__name__} for {self._moonboard.get_year_layout()} {self._moonboard.__class__.__name__}"

    def _map_row_to_image(self, row: str) -> int:
        """
        Map a board row value to the corresponding image row value

        Args:
            row (str): Row value to map

        Returns:
            int: Row in image coordinates
        """
        return ord(row.lower()) - ord('a')

    def _map_col_to_image(self, col: str) -> int:
        """
        Map a board column value to the corresponding image column value

        Args:
            col (str): Column value to map

        Returns:
            int: Column in image coordinates
        """
        if isinstance(col, str):
            col = int(col)
        return self._moonboard._rows - col

    def _map_coordinates_to_image(self, row: str, col: str) -> Tuple[int, int]:
        """Map row and column Moonboard coordinates to image coordinates

        Args:
            row (str): Row to map
            col (str): Column to map

        Returns:
            tuple: Row, Column in image coordinates
        """
        i = self._map_row_to_image(row)
        j = self._map_col_to_image(col)
        return (i, j)

    def _get_text(self, problem: dict) -> str:
        """
        Add a short text indicating the problem name and grade

        Args:
            problem (dict): Moonboard problem info

        Returns:
            str: Text to add to the rendered image
        """
        benchmark = ', Benchmark' if problem.get('IsBenchmark', '') else ''
        return f"{problem.get('Name', '')}, {problem.get('Grade', '')}{benchmark}"

    def _draw_problem_moves(self, draw: ImageDraw, problem: dict) -> ImageDraw:
        """
        Draw problem moves into the Moonboard layout

        Args:
            draw (ImageDraw): ImageDraw object to draw on
            problem (dict): Problem info

        Returns:
            ImageDraw: Modified ImageDraw object with problem moves drawn
        """
        for move in problem['Moves']:
            typeof_move = 'start' if move['IsStart'] else (
                'top' if move['IsEnd'] else 'middle')
            i, j = self._map_coordinates_to_image(
                move['Description'][:1], move['Description'][1:])
            draw.ellipse(
                [
                    self._render_config._offset_x +
                    self._render_config._bbox_side * i,
                    self._render_config._offset_y +
                    self._render_config._bbox_side * j,
                    self._render_config._offset_x +
                    self._render_config._bbox_side * (i+1),
                    self._render_config._offset_y +
                    self._render_config._bbox_side * (j+1)
                ],
                fill=None,
                outline=self._render_config._color_map[typeof_move],
                width=self._render_config._circle_width
            )
        return draw

    def _write_problem_info(self, draw: ImageDraw, problem: dict) -> ImageDraw:
        """
        Draw problem name, grade and benchmark status on the image

        Args:
            draw (ImageDraw): Image draw object where the problem is rendered
            problem (dict): Data of the problem to render

        Returns:
            ImageDraw: Modified ImageDraw object with the problem 
            information (name, grade and benchmark status) rendered
        """
        fnt = ImageFont.truetype(
            self._render_config._font, self._render_config._text_size)
        info_text = self._get_text(problem)
        draw.text(
            self._render_config._text_position,
            info_text,
            self._render_config._text_color,
            font=fnt
        )

    def render_problem(self, problem: dict, with_info: bool = False, show: bool = True, save: bool = False) -> Image:
        """
        Render a Moonboard problem

        Args:
            problem (dict): problem data, in the format returned by querying the moonboard page
            with_info (bool, optional): Add problem info to rendered image. Defaults to False.
            show (bool, optional): Show the rendered problem in the screen. Defaults to True.
            save (bool, optional): Save image file. Defaults to False.

        Returns:
            Image: The Rendered problem
        """
        with Image.open(self._moonboard._image) as im:
            draw = ImageDraw.Draw(im)
            draw = self._draw_problem_moves(draw, problem)
            if with_info:
                self._write_problem_info(draw, problem)
            if show:
                im.show()
            if save:
                im.save(f"{problem.get('Name', 'Unknown')}.png", 'PNG')
            return im


if __name__ == "__main__":
    # Create Renderer
    config = RendererConfig()
    renderer = ProblemRenderer(get_moonboard(2017), config)
    # Load data
    with open('problems.json', 'r') as f:
        problems = json.load(f)

    renderer.render_problem(problems['339318'], with_info=True)

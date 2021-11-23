from typing import Tuple
from moonboard import BaseProblemAdapter, MoonBoard, RendererConfig
from PIL import Image, ImageDraw, ImageFont


class ProblemRenderer():
    """
    Generic class to render a problem on a board
    """

    def __init__(self, moonboard_layout: MoonBoard, problem_adapter: BaseProblemAdapter, render_config: RendererConfig) -> None:
        """
        Initialize a ProblemRenderer object.

        Args:
            moonboard_layout (MoonBoard): Layout of the Moonboard to render on.
            problem_adapter (BaseProblemAdapter): Object that knows how to map raw data to a Problem object.
            render_config (RendererConfig): Config for rendering Moonboard Problems
        """
        self._moonboard = moonboard_layout
        self._render_config = render_config
        self._problem_adapter = problem_adapter

    def __str__(self) -> str:
        """
        User friendly representation of the ProblemRenderer object

        Returns:
            str: string representation of the ProblemRenderer object
        """
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
        """
        Map row and column Moonboard coordinates to image coordinates

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

from typing import Any, Tuple
from models.problem import Problem
from moonboard import BaseProblemAdapter, MoonBoard
from render_config import RendererConfig
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

    def _map_row_to_image(self, row: int) -> int:
        """
        Map a board row value to the corresponding image row value

        Args:
            row (int): Row value to map

        Returns:
            int: Row in image coordinates
        """
        return self._moonboard._rows - row

    def _map_col_to_image(self, col: int) -> int:
        """
        Map a board column value to the corresponding image column value

        Args:
            col (int): Column value to map

        Returns:
            int: Column in image coordinates
        """
        return col

    def _map_coordinates_to_image(self, row: int, col: int) -> Tuple[int, int]:
        """
        Map row and column Moonboard coordinates to image coordinates

        Args:
            row (int): Row to map
            col (int): Column to map

        Returns:
            tuple: Row, Column in image coordinates
        """
        i = self._map_row_to_image(row)
        j = self._map_col_to_image(col)
        return (j, i)

    def _get_text(self, problem: Problem) -> str:
        """
        Add a short text indicating the problem name and grade

        Args:
            problem (Problem): Moonboard problem info

        Returns:
            str: Text to add to the rendered image
        """
        benchmark = ', Benchmark' if problem.is_benchmark else ''
        return f"{problem.name}, {problem.grade}{benchmark}"

    def _draw_problem_moves(self, draw: ImageDraw, problem: Problem) -> ImageDraw:
        """
        Draw problem moves into the Moonboard layout

        Args:
            draw (ImageDraw): ImageDraw object to draw on
            problem (Problem): Problem info

        Returns:
            ImageDraw: Modified ImageDraw object with problem moves drawn
        """
        for move in problem.moves:
            typeof_move = 'start' if move.is_start else (
                'top' if move.is_end else 'middle')
            i, j = self._map_coordinates_to_image(
                move.row, move.column)
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

    def _write_problem_info(self, draw: ImageDraw, problem: Problem) -> ImageDraw:
        """
        Draw problem name, grade and benchmark status on the image

        Args:
            draw (ImageDraw): Image draw object where the problem is rendered
            problem (Problem): Data of the problem to render

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

    def render_problem(self, problem: Any, with_info: bool = False, show: bool = True, save: bool = False) -> Image:
        """
        Render a Moonboard problem

        Args:
            problem: problem data, in the format returned by querying the moonboard page
            with_info (bool, optional): Add problem info to rendered image. Defaults to False.
            show (bool, optional): Show the rendered problem in the screen. Defaults to True.
            save (bool, optional): Save image file. Defaults to False.

        Returns:
            Image: The Rendered problem
        """
        parsed_problem = self._problem_adapter.map_problem(problem)
        with Image.open(self._moonboard._image) as im:
            draw = ImageDraw.Draw(im)
            draw = self._draw_problem_moves(draw, parsed_problem)
            if with_info:
                self._write_problem_info(draw, parsed_problem)
            if show:
                im.show()
            if save:
                im.save(f"{parsed_problem.name}.png", 'PNG')
            return im

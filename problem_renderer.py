from typing import Any, Tuple
from models.problem import Problem
from moonboard import BaseProblemAdapter, MoonBoard
from render_config import RendererConfig
from PIL import Image, ImageDraw, ImageFont


class ProblemRenderer():
    """
    Generic class to render a problem on a board

    :param moonboard_layout: Layout of the Moonboard to render on.
    :type moonboard_layout: MoonBoard
    :param problem_adapter: Object that knows how to map raw data to a Problem object.
    :type problem_adapter: BaseProblemAdapter
    :param render_config: Config for rendering Moonboard Problems
    :type render_config: RendererConfig
    """

    def __init__(self, moonboard_layout: MoonBoard, problem_adapter: BaseProblemAdapter, render_config: RendererConfig) -> None:
        """
        Initialize a ProblemRenderer object
        """
        self._moonboard = moonboard_layout
        self._render_config = render_config
        self._problem_adapter = problem_adapter

    def __str__(self) -> str:
        """
        User friendly representation of the ProblemRenderer object
        """
        return f"{__class__.__name__} for {self._moonboard.get_year_layout()} {self._moonboard.__class__.__name__}"

    def _map_row_to_image(self, row: int) -> int:
        """
        Map a board row value to the corresponding image row value

        :param row: Row value to map
        :type row: int
        :return: Row in image coordinates
        :rtype: int
        """
        return self._moonboard._rows - row

    def _map_col_to_image(self, col: int) -> int:
        """
        Map a board column value to the corresponding image column value
        :param col: Column value to map
        :type col: int
        :return: Column in image coordinates
        :rtype: int
        """
        return col

    def _map_coordinates_to_image(self, row: int, col: int) -> Tuple[int, int]:
        """
        Map row and column Moonboard coordinates to image coordinates
        :param row: Row value to map
        :type row: int
        :param col: Column value to map
        :type col: int
        :return: Row and column in image coordinates
        :rtype: Tuple[int, int]
        """
        i = self._map_row_to_image(row)
        j = self._map_col_to_image(col)
        return (j, i)

    def _get_text(self, problem: Problem) -> str:
        """
        Add a short text indicating the problem name and grade

        :param problem: Problem data
        :type problem: Problem
        :return: Text to be rendered
        :rtype: str
        """
        benchmark = ', Benchmark' if problem.is_benchmark else ''
        return f"{problem.name}, {problem.grade}{benchmark}"

    def _draw_problem_moves(self, draw: ImageDraw, problem: Problem) -> ImageDraw:
        """
        Draw problem moves into the Moonboard layout
        :param draw: ImageDraw object where the problem is rendered
        :type draw: ImageDraw
        :param problem: Problem data
        :type problem: Problem
        :return: Modified ImageDraw object with the problem moves rendered
        :rtype: ImageDraw
        """
        for move in problem.moves:
            typeof_move = 'start' if move.is_start else (
                'top' if move.is_end else 'middle')
            i, j = self._map_coordinates_to_image(
                move.row, move.column)
            draw.ellipse(
                [
                    self._render_config.offset_x +
                    self._render_config.bbox_side * i,
                    self._render_config.offset_y +
                    self._render_config.bbox_side * j,
                    self._render_config.offset_x +
                    self._render_config.bbox_side * (i+1),
                    self._render_config.offset_y +
                    self._render_config.bbox_side * (j+1)
                ],
                fill=None,
                outline=self._render_config.color_map[typeof_move],
                width=self._render_config.circle_width
            )
        return draw

    def _write_problem_info(self, draw: ImageDraw, problem: Problem) -> ImageDraw:
        """
        Draw problem name, grade and benchmark status on the image

        :param draw: ImageDraw object where the problem is rendered
        :type draw: ImageDraw
        :param problem: Problem data
        :type problem: Problem
        :return: Modified ImageDraw object with the problem information (name, grade and benchmark status) rendered
        """
        fnt = ImageFont.truetype(
            self._render_config.font, self._render_config.text_size)
        info_text = self._get_text(problem)
        draw.text(
            self._render_config.text_position,
            info_text,
            self._render_config.text_color,
            font=fnt
        )

    def render_problem(self, problem: Any, with_info: bool = False, show: bool = True, save: bool = False) -> Image:
        """
        Render a Moonboard problem

        :param problem: Problem data
        :param with_info: If True, render problem name, grade and benchmark status along the problem. False by default.
        :type with_info: bool
        :param show: If True, show the rendered image. True by default.
        :type show: bool
        :param save: If True, save the rendered image. True by default
        :type save: bool
        :return: Rendered image
        :rtype: Image
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

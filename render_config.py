from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class RendererConfig:
    """
    Class for keeping the configuration parameters of the renderer
    Default values are set for the following board layouts: 2016, 2017, 2019

    :param color_map: Color map to use for the moves
    :type color_map: Dict[str, Tuple[str, str]]
    :param bbox_side: Side of the bounding box for the circle that highlights a move
    :type bbox_side: float
    :param offset_x: x-axis distance between consecutive holds
    :type offset_x: float
    :param offset_y: x-axis distance between consecutive holds
    :type offset_y: float
    :param circle_width: Width of the circle that highlights a move in pixels
    :type circle_width: float
    :param text_size: Size of the text to write in pixels
    :type text_size: int
    :param text_position: Position of the text to write
    :type text_position: Tuple[float, float]
    :param text_color: Color of the text to write
    :type text_color: Tuple[int, int, int]
    :param font: Font to use for the text. Tbe font refered here must be installed on the system or located under fonts
    :type font: str
    """
    # colors for different type of holds
    color_map: Dict[str, Tuple[int, int, int]] = field(default_factory=lambda: {
        'start': (0, 255, 0),  # green
        'middle': (0, 0, 255),  # blue
        'top': (255, 0, 0)  # red
    })
    # geometry of board images
    bbox_side: float = 51.5
    offset_x: float = 70
    offset_y: float = 60
    circle_width: float = 7
    # text configuration for rendering problem name
    text_size: int = 30
    text_position: Tuple[float, float] = (15, 980)
    text_color: Tuple[int, int, int] = (255, 255, 255)
    font: str = "fonts/MilkyNice.ttf"

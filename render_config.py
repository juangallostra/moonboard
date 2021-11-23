from dataclasses import dataclass, field
from typing import Dict, Tuple

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

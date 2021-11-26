from PIL import Image, ImageDraw, ImageFont
import json


class DrawBoard():
    def __init__(self, rows, columns, image_path=None):
        self._rows = rows
        self._columns = columns
        self._image_path = image_path
        # colors for different type of holds
        self._color_map = {
            'start': (0, 255, 0),  # green
            'middle': (0, 0, 255),  # blue
            'top': (255, 0, 0)  # red
        }
        self._text_size = 30

    def _map_coordinates(self):
        """
        Should map board row and col to image x y coordinates 
        """
        raise NotImplementedError

    def _get_info_text(self):
        """
        Should return the position, text and color to be written
        on the image
        """
        raise NotImplementedError

    def render_problem(self, problem, with_info=False, show=True, save=False):
        with Image.open(self._image_path) as im:
            draw = ImageDraw.Draw(im)
            for move in problem['Moves']:
                typeof_move = 'start' if move['IsStart'] else (
                    'top' if move['IsEnd'] else 'middle')
                i, j = self._map_coordinates(
                    move['Description'][:1], move['Description'][1:])
                draw.ellipse(
                    [
                        self._offset_x + self._bbox_side*(i),
                        self._offset_y + self._bbox_side*(j),
                        self._offset_x + self._bbox_side*(i+1),
                        self._offset_y + self._bbox_side*(j+1)
                    ],
                    fill=None,
                    outline=self._color_map[typeof_move],
                    width=self._circle_width
                )
            if with_info:
                fnt = ImageFont.truetype(
                    "fonts/MilkyNice.ttf", self._text_size)
                pos, info_text, color = self._get_info_text(problem)
                draw.text(
                    pos,
                    info_text,
                    color,
                    font=fnt
                )
            if show:
                im.show()
            if save:
                im.save('test.png', 'PNG')


class MoonboardRenderer(DrawBoard):
    def __init__(self):
        super().__init__(rows=18, columns=11)
        # geometry of board images
        self._bbox_side = 51.5
        self._offset_x = 70
        self._offset_y = 60
        self._circle_width = 7
        # image files
        self._path_to_images = 'moonboards/'
        self._moonboard_version_to_image = {
            2016: 'mbsetup-2016.jpg',
            2017: 'mbsetup-mbm2017.jpg',
            2019: 'mbsetup-mbm2019.jpg'
        }
        self._current_version = 2017
        self._image_path = self.get_moonboard_image_path()

    def _map_coordinates(self, row, col):
        if isinstance(col, str):
            col = int(col)
        return (ord(row.lower()) - ord('a'), self._rows - col)

    def _get_info_text(sel, problem):
        benchmark = ', Benchmark' if problem.get('IsBenchmark', '') else ''
        return (15, 980), "{}, {}{}".format(problem['Name'], problem['Grade'], benchmark), (255, 255, 255)

    def set_moonboard_version(self, version):
        if version not in self._moonboard_version_to_image.keys():
            return  # TODO: Warn that the version is not valid
        self._current_version = version
        # update image path
        self._image_path = self.get_moonboard_image_path()

    def get_current_version(self):
        return self._current_version

    def get_moonboard_image_path(self):
        return self._path_to_images + self._moonboard_version_to_image[self._current_version]


if __name__ == "__main__":
    # Test with a sample problem
    with open('problems.json', 'r') as f:
        problems = json.load(f)
    a = MoonboardRenderer()
    a.set_moonboard_version(2017)
    counter = 0
    for problem in problems:
        if counter == 0:
            break
        a.render_problem(problems[problem], with_info=True)
        counter += 1
    # a.render_problem(problems['341209'])
    # a.render_problem(problems['341207'])
    # a.render_problem(problems['341203'])
    a.render_problem(problems['339318'], with_info=True)

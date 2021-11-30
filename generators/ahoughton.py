from typing import Any, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from generators.base_generator import BaseGenerator
from selenium.webdriver.common.by import By


class AhoughtonGenerator(BaseGenerator):
    """
    Generate problems from the Ahoughton website. 
    Inherits from BaseGenerator, which assumes the class
    implements a generate() method.

    :param year: Moonboard layout year for which we want to generate problems. Defaults to 2016.
    :type year: int, optional
    """

    def __init__(self, year: int = 2016) -> None:
        # CSS selectors used to identify the elements on the page
        # Directly extracted from the website
        self.MOVE_CSS_CLASS = 'm-fadeIn'
        self.GENERATE_BUTTON_CSS_CLASS = 'red'
        self.CSS_MOONBOARD_LAYOUT_SELECTORS = {
            2016: 'div.option:nth-child(1) > label:nth-child(2) > input:nth-child(1)',
            2017: 'div.option:nth-child(1) > label:nth-child(3) > input:nth-child(1)'
        }
        self.year = year
        super().__init__()

    def _configure_chrome_driver(self, *args, headless: bool = True) -> Options:
        """
        Set and return the configuration of the driver used to load the page
        and generate a new problem. This is a Chrome-specific configuration.
        It disables browser extensions and gpu and sets the headless option to True. 

        :param *args: arguments to pass to the driver
        :param headless: whether to launch the browser driver in headless mode. Defaults to True.
        :type headless: bool, optional
        :return: driver configuration options
        :rtype: Options
        """
        chrome_options = Options()
        chrome_options.headless = headless
        for arg in args:
            chrome_options.add_argument(arg)
        return chrome_options

    def _get_chrome_driver(self, path: str = 'C:/.selenium_drivers/chromedriver.exe') -> webdriver:
        """
        Get the configured driver used to load the page and generate a new problem.

        :param path: driver path, defaults to 'C:/.selenium_drivers/chromedriver.exe'
        :type path: str, optional
        :return: the configured driver
        :rtype: webdriver
        """
        return webdriver.Chrome(
            service=Service(path),
            options=self._configure_chrome_driver(
                "--disable-extensions",
                "--disable-gpu",
                headless=True
            )
        )

    def _parse_moves(self, moves: List[Any]) -> List[str]:
        """
        Given the list of moves extracted from the website, parse them into a list of strings
        where each element are the coordinates of a hold from the problem.

        :param moves: List of moves extracted from the website html
        :type moves: List[Any]
        :return: Processed list of moves as moonboard coordinates (['D18', 'G13', ...])
        :rtype: List[str]
        """
        parsed_moves = []
        for move in moves:
            move_coords = move.get_attribute('id')  # D18 or whatever
            parsed_moves.append(move_coords)
        return parsed_moves


    def generate(self) -> str:
        """
        Generate a new problem from the Ahoughton website.

        :return: The problem generated by the website
        :rtype: str
        """
        driver = self._get_chrome_driver()
        driver.get("https://ahoughton.com/moon")
        # Select moonboard layout
        driver.find_element(By.CSS_SELECTOR, self.CSS_MOONBOARD_LAYOUT_SELECTORS[self.year]).click()
        # generate a new climb
        driver.find_elements(By.CLASS_NAME, self.GENERATE_BUTTON_CSS_CLASS)[0].click()
        # get moves
        moves = driver.find_elements(By.CLASS_NAME, self.MOVE_CSS_CLASS)
        # Quit the driver
        # driver.quit()
        return self._parse_moves(moves)

from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from generators.base_generator import BaseGenerator


class AhoughtonGenerator(BaseGenerator):
    """[summary]

    :param BaseGenerator: [description]
    :type BaseGenerator: [type]
    """

    def __init__(self, ) -> None:
        """[summary]
        """
        self.name = 'ahoughton'
        super().__init__()

    def _configure_chrome_driver(self, args_to_add: List[str]) -> Options:
        """
        Set and return the configuration of the driver used to load the page
        and generate a new problem. This is a Chrome-specific configuration.
        It disables browser extensions and gpu and sets the headless option to True. 

        :param args: arguments to pass to the driver
        :type args: List[str]
        :return: driver configuration options
        :rtype: Options
        """
        chrome_options = Options()
        for arg in args_to_add:
            chrome_options.add_argument(arg)
        return chrome_options

    def _get_driver(self, path: str = 'C:/.selenium_drivers/chromedriver.exe') -> webdriver:
        """
        Get the configured driver used to load the page and generate a new problem.

        :param path: driver path, defaults to 'C:/.selenium_drivers/chromedriver.exe'
        :type path: str, optional
        :return: the configured driver
        :rtype: webdriver
        """
        return webdriver.Chrome(
            path,
            options=self._configure_chrome_driver(
                [
                    "--disable-extensions",
                    "--disable-gpu",
                    "--headless"
                ]
            )
        )

    def generate(self):
        """[summary]
        """
        from selenium.webdriver.common.by import By
        driver = self._get_driver()
        driver.get("https://ahoughton.com/moon")
        # generate a new climb
        driver.find_elements(By.CLASS_NAME, 'red')[0].click()
        # get moves
        moves = driver.find_elements(By.CLASS_NAME, 'm-fadeIn')
        parsed_moves = []
        for move in moves:
            move_coords = move.get_attribute('id')  # D18 or whatever
            parsed_moves.append(move_coords)
        return parsed_moves

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from generators.base_generator import BaseGenerator

class AhoughtonGenerator(BaseGenerator):
    def __init__(self) -> None:
        self.name = 'ahoughton'
        super().__init__()

    def _configure_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        return chrome_options

    def _get_driver(self):
        return webdriver.Chrome(
            'C:/.selenium_drivers/chromedriver.exe', 
            options=self._configure_chrome_driver()
        )
        # driver = webdriver.Firefox('C:/.selenium_drivers/geckodriver.exe')
        # driver = webdriver.Firefox('C:/.selenium_drivers/geckodriver.exe')

    def load_page(self):
        driver = self._get_driver()
        driver.get("https://ahoughton.com/moon")
        # generate a new climb
        driver.find_elements_by_class_name('red')[0].click()
        # get moves
        moves = driver.find_elements_by_class_name('m-fadeIn')
        parsed_moves = []
        for move in moves:
            move_coords = move.get_attribute('id') # D18 or whatever
            parsed_moves.append(move_coords)
        print(parsed_moves) # <- List of moves

    def generate(self):
        pass


if __name__ == '__main__':
    a = AhoughtonGenerator()
    a.load_page()
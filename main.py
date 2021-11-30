from generators.ahoughton import AhoughtonGenerator
from render_config import RendererConfig
from problem_renderer import ProblemRenderer
from moonboard import get_moonboard
from adapters.default import DefaultProblemAdapter
from adapters.crg import CRGProblemAdapter
from adapters.ahoughton import AhoughtonAdapter
import json


def main():
    # Create Renderer
    config = RendererConfig()
    renderer = ProblemRenderer(
        get_moonboard(2017), 
        DefaultProblemAdapter(), 
        config
    )
    crg_renderer = ProblemRenderer(
        get_moonboard(2017), 
        CRGProblemAdapter(), 
        config
    )
    
    ahoughton_renderer_2016 = ProblemRenderer(
        get_moonboard(2016),
        AhoughtonAdapter(),
        config
    )
    ahoughton_generator_2016 = AhoughtonGenerator(year=2016, driver_path='C:/.selenium_drivers/chromedriver.exe')

    ahoughton_renderer_2017 = ProblemRenderer(
        get_moonboard(2017),
        AhoughtonAdapter(),
        config
    )
    ahoughton_generator_2017 = AhoughtonGenerator(year=2017, driver_path='C:/.selenium_drivers/chromedriver.exe')
    
    # Load data
    with open('data/problems.json', 'r') as f:
        problems = json.load(f)
        renderer.render_problem(problems['339318'], with_info=True)
    with open('data/crg.json', 'r') as f:
        crg_problems = json.load(f)
        crg_renderer.render_problem(crg_problems['1'])
    # Ahoughton generator and adapter test
    # 2016
    problem = ahoughton_generator_2016.generate()
    ahoughton_renderer_2016.render_problem(problem)
    # 2017
    problem = ahoughton_generator_2017.generate()
    ahoughton_renderer_2017.render_problem(problem)
    

if __name__ == "__main__":
    main()

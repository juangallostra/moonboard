from render_config import RendererConfig
from problem_renderer import ProblemRenderer
from moonboard import get_moonboard
from adapters.default import DefaultProblemAdapter
from adapters.crg import CRGProblemAdapter
import json

def main():
    # Create Renderer
    config = RendererConfig()
    renderer = ProblemRenderer(get_moonboard(2017), DefaultProblemAdapter(), config)
    crg_renderer = ProblemRenderer(get_moonboard(2017), CRGProblemAdapter(), config)
    # Load data
    with open('problems.json', 'r') as f:
        problems = json.load(f)
        renderer.render_problem(problems['339318'], with_info=True)
    with open('crg.json', 'r') as f:
        crg_problems = json.load(f)
        crg_renderer.render_problem(crg_problems['1'])


if __name__ == "__main__":
    main()
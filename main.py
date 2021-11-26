from render_config import RendererConfig
from problem_renderer import ProblemRenderer
from moonboard import get_moonboard
from moonboard import DefaultProblemAdapter
import json

def main():
    # Create Renderer
    config = RendererConfig()
    renderer = ProblemRenderer(get_moonboard(2017), DefaultProblemAdapter(), config)
    # Load data
    with open('problems.json', 'r') as f:
        problems = json.load(f)

    renderer.render_problem(problems['339318'], with_info=True)

if __name__ == "__main__":
    main()
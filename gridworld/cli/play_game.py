import fire
from loguru import logger

from gridworld.models import Game


def play_game(world_width: int = 4, world_height: int = 4, start_cell: int = 0, goal_cell: int = 15,
              obstacles_cells=None, policy_search_iterations: int = 200000, value_search_iterations: int = 100000,
              threshold: float = 1e-20, gamma: float = 0.8) -> None:
    """
    Makes an agent solve a world with the specifications given by the user.

    Parameters
    ----------
    world_width: int
        World's width in cells.
    world_height: int
        World's height in cells.
    start_cell: int
        Cell where the agent will start.
    goal_cell: int
        Cell where the agent has to go.
    obstacles_cells: list
        Cells where obstacles will be placed.
    policy_search_iterations: int
        Maximum number of iterations when looking for optimal policy.
    value_search_iterations: int
        Maximum number of iterations when looking for optimal state-value function.
    threshold: float
        Minimum change that should happen to continue value search iteration.
    gamma: float
        Discount factor
    """
    if obstacles_cells is None:
        obstacles_cells = [5, 7, 11, 12]

    game = Game(world_width=world_width, world_height=world_height, start_cell=start_cell, goal_cell=goal_cell,
                obstacles_cells=obstacles_cells)
    game.play(policy_search_iterations=policy_search_iterations, value_search_iterations=value_search_iterations,
              threshold=threshold, gamma=gamma)


@logger.catch
def main():
    fire.Fire(play_game)


if __name__ == "__main__":
    main()

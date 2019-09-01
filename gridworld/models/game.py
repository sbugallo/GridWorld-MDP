from typing import List, Tuple

from loguru import logger

from .agent import Agent
from .world import World


class Game:
    """
    Models a simple game where an agent tries to solve a grid world with the given configuration

    Parameters
    ----------
    world: gridworld.models.World
        Board to be solved.
    agent: gridworld.models.Agent
        Agent that will solve the board.
    """

    def __init__(self, world_width: int, world_height: int, start_cell: int, goal_cell: int,
                 obstacles_cells: List[int]) -> None:
        """

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
        """

        self.world = World(grid_width=world_width, grid_height=world_height, starting_position=start_cell,
                           goal_position=goal_cell, obstacle_positions=obstacles_cells)

        self.agent = Agent()

    def play(self, policy_search_iterations: int = 200000, value_search_iterations: int = 100000,
             threshold: float = 1e-20, gamma: float = 0.8) -> Tuple[list, bool]:
        """
        Makes agent solve the board.

        Parameters
        ----------
        policy_search_iterations: int
            Maximum number of iterations when looking for optimal policy.
        value_search_iterations: int
            Maximum number of iterations when looking for optimal state-value function.
        threshold: float
            Minimum change that should happen to continue value search iteration.
        gamma: float
            Discount factor

        Returns
        -------
        player_positions: list
            Cells the agent followed.
        reached_goal: bool
            True if agent reached goal cell successfully, False otherwise.
        """

        logger.info("Beginning agent training")
        self.agent.environment = self.world
        self.agent.run_value_iteration(value_search_iterations, threshold, gamma)
        self.agent.run_policy_iteration(policy_search_iterations, gamma)
        self.agent.plot_q_function()

        logger.info("Solving game")
        player_positions, reached_goal = self.agent.solve()

        custom = []
        for step in player_positions:
            custom.append(step)
            self.world.print(custom[1:-1])

        self.world.print(player_positions[1:-1])

        if reached_goal:
            logger.info(f"Agent solved the problem in {len(player_positions) - 1} moves!")
        else:
            logger.info(f"Agent could not solve the problem!")

        return player_positions, reached_goal

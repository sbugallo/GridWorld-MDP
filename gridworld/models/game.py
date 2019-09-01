from loguru import logger

from .agent import Agent
from .world import World


class Game:

    def __init__(self, word_width, world_height, start_cell, goal_cell, obstacles_cells):

        self.world = World(grid_width=word_width, grid_height=world_height, starting_position=start_cell,
                           goal_position=goal_cell, obstacle_positions=obstacles_cells)

        self.agent = Agent()

    def play(self, policy_search_iterations: int = 200000, value_search_iterations: int = 100000,
             threshold: float = 1e-20, gamma: float = 0.8):

        logger.info("Beginning agent training")
        self.agent.environment = self.world
        self.agent.run_value_iteration(value_search_iterations, threshold, gamma)
        self.agent.run_policy_iteration(policy_search_iterations, gamma)
        self.agent.plot_q_function()

        logger.info("Solving game")
        player_positions, reached_goal = self.agent.solve()

        self.world.print(player_positions[1:-1])

        if reached_goal:
            logger.info(f"Agent solved the problem in {len(player_positions) - 1} moves!")
        else:
            logger.info(f"Agent could not solve the problem!")

        return player_positions, reached_goal

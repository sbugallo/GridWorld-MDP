import numpy as np
from colorama import init, Back
from loguru import logger

from .action import Action
from .reward import Reward
from .state import State


class World:
    """
    Class modeling the world.

    Attributes
    ----------
    grid : list
        List with world's elements.
    grid_width: int
            Grid's width in cells.
    grid_height: int
        Grid's height in cells
    starting_position: int
        Cell where the agent will be place at the start.
    goal_position: int
        Cell where the agent has to go.
    obstacle_positions: list
        Cells where obstacles will be placed.
    """

    def __init__(self, grid_width: int = 4, grid_height: int = 4, starting_position: int = 0, goal_position: int = 15,
                 obstacle_positions: list = None) -> None:
        """
        Parameters
        ----------
        grid_width: int
            Grid's width in cells.
        grid_height: int
            Grid's height in cells
        starting_position: int
            Cell where the agent will be place at the start.
        goal_position: int
            Cell where the agent has to go.
        obstacle_positions: list
            Cells where obstacles will be placed.
        num_states = int
            Number of states in this world

        Raises
        ------
        ValueError:
            If any element is incompatible with the world.
        """

        if obstacle_positions is None:
            self.obstacle_positions = [5, 7, 11, 12]
        else:
            self.obstacle_positions = obstacle_positions

        self.grid_height = grid_height
        self.grid_width = grid_width
        self.num_states = grid_width * grid_height
        self.starting_position = starting_position
        self.goal_position = goal_position

        self.grid = np.zeros((self.grid_height * self.grid_width), dtype=int)

        if self.starting_position not in range(self.grid_width * self.grid_height):
            raise ValueError(f"Starting cell {self.starting_position} is not valid")

        self.grid[self.starting_position] = 1

        if self.goal_position not in range(self.grid_width * self.grid_height) or self.grid[self.goal_position] != 0:
            raise ValueError(f"Goal cell {self.goal_position} is not valid.")
        self.grid[self.goal_position] = 2

        for obstacle in self.obstacle_positions:
            if obstacle not in range(self.grid_width * self.grid_height) or self.grid[obstacle] != 0:
                raise ValueError(f"Obstacle cell {obstacle} is not valid.")

        self.grid[self.obstacle_positions] = -1

        self._compute_world_params()

    def _compute_world_params(self) -> None:
        """Computes results of applying every action to each cell."""

        self.states = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                cell = row * self.grid_width + col
                cell_type = self.grid[cell]

                possible_actions = {
                    Action.up: self._get_action(max(row - 1, 0) * self.grid_width + col),
                    Action.down: self._get_action(min(row + 1, self.grid_height - 1) * self.grid_width + col),
                    Action.right: self._get_action(row * self.grid_width + min(col + 1, self.grid_width - 1)),
                    Action.left: self._get_action(row * self.grid_width + max(col - 1, 0))
                }

                self.states.append(State(cell, possible_actions, cell_type))

    def get_state(self, cell_id: int) -> State:
        """
        Retrieves the state of the given `cell_id`.

        Parameters
        ----------
        cell_id: int
            ID of the cell.

        Returns
        -------
        cells_state: gridworld.models.State
        """
        return self.states[cell_id]

    def _get_action(self, next_cell: int) -> dict:
        """
        Generates action results.

        Parameters
        ----------
        next_cell: int
            Cell ID where agent will be placed after performing the action

        Returns
        -------
        action_results: dict
            Format: {"transition_probability": int, "reward": float, "cell_id": int, "is_goal": bool}

        """
        next_cell_type = self.grid[next_cell]

        if next_cell_type == 0 or next_cell_type == 1:
            reward = Reward.road.value
        elif next_cell_type == 2:
            reward = Reward.goal.value
        else:
            reward = Reward.obstacle.value * self.num_states

        return {
            "transition_probability": 1.0,
            "reward": reward,
            "cell_id": next_cell,
            "is_goal": next_cell == self.goal_position,
        }

    def print(self, player_positions: list = None) -> list:
        """
        Prints world's grid and players positions.

        Parameters
        ----------
        player_positions: list
            Cells the player has be in except start and goal cells.

        Returns
        -------
        colored_grid: list
            List with color value of each cell
        """

        if player_positions is None:
            player_positions = []

        init(autoreset=True)
        element_to_color = {-1: Back.RED, 0: Back.WHITE, 1: Back.GREEN, 2: Back.BLUE}

        board_text = ""
        colored_grid = []
        for row in range(self.grid_height):
            row_text = "\n"

            for col in range(self.grid_width):
                cell_id = row * self.grid_width + col
                if cell_id in player_positions:
                    cell_color = Back.CYAN
                else:
                    cell_value = self.grid[cell_id]
                    cell_color = element_to_color[cell_value]

                colored_grid.append(cell_color)

                if col == self.grid_width - 1:
                    row_text += f" {cell_color}   {Back.RESET}"
                else:
                    row_text += f" {cell_color}   {Back.RESET} |"

            if row != self.grid_height - 1:
                divider = "\n"
                for cell in range(self.grid_width):

                    if cell != self.grid_width - 1:
                        divider += "------"
                    else:
                        divider += "-----"

                row_text += divider

            board_text += row_text

        logger.info(board_text)
        return colored_grid

import numpy as np
from colorama import init, Back
from loguru import logger

from .action import Action


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

    def _compute_world_params(self):

        reshaped_grid = self.grid.reshape((self.grid_height, self.grid_width))
        self.top_boundary_cells = reshaped_grid[0, :]
        self.bottom_boundary_cells = reshaped_grid[-1, :]
        self.left_boundary_cells = reshaped_grid[:, 0].T
        self.right_boundary_cells = reshaped_grid[:, -1].T

        self.top_left_corner_cell = self.top_boundary_cells[0]
        self.top_right_corner_cell = self.top_boundary_cells[-1]
        self.bottom_left_corner_cell = self.bottom_boundary_cells[0]
        self.bottom_right_corner_cell = self.bottom_boundary_cells[-1]

        self.states = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                cell = row * self.grid_width + col

                possible_actions = {}

                if cell not in self.top_boundary_cells:
                    possible_actions[Action.up] = {
                        "transition_probability": 1.0,
                        "reward": 1,
                        "next_state": (row - 1) * self.grid_width + col,
                        "is_goal": cell == self.goal_position,
                    }

                if cell not in self.bottom_boundary_cells:
                    possible_actions[Action.bottom] = (row + 1) * self.grid_width + col

                if cell not in self.right_boundary_cells:
                    possible_actions[Action.right] = row * self.grid_width + (col + 1)

                if cell not in self.left_boundary_cells:
                    possible_actions[Action.left] = row * self.grid_width + (col - 1)

                self.states.append(State(cell, )

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

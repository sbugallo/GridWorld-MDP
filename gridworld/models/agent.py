import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
from mpl_toolkits.mplot3d import Axes3D  # noqa:F401

from .action import Action
from .world import World


class Agent:
    """
    Models a Markov Decision Process-based agent.

    Parameters
    ----------
    policy: numpy.ndarray
    state_value_function: numpy.ndarray
    q_function: dict
    environment: gridworld.models.World
    """
    def __init__(self):
        self.policy: np.ndarray = np.array([])
        self.state_value_function: np.ndarray = np.array([])
        self.q_function: dict = {}
        self.environment: World = World()

    def run_value_iteration(self, max_iterations: int = 100000, threshold: float = 1e-20, gamma=0.99) -> None:
        """
        Estimates optimal state-value function.

        Parameters
        ----------
        max_iterations: float
            Maximum number of iterations when looking for state-value function.
        threshold: float
            Minimum change that should happen to continue value search iteration.
        gamma: float
            Discount factor
        """

        logger.info("\t- Starting value iteration")
        values = np.zeros(self.environment.num_states)
        q_function = {}

        for iteration in range(max_iterations):
            old_values = values.copy()
            for state in range(self.environment.num_states):
                q_values = {}
                state = self.environment.get_state(state)

                for action in state.actions:
                    next_state_data = state.get_action_results(action)

                    reward = next_state_data["transition_probability"] * (
                            next_state_data["reward"] + gamma * old_values[next_state_data["cell_id"]])
                    q_values[action.value] = reward

                values[state.cell_id] = np.max(list(q_values.values()))
                q_function[state.cell_id] = q_values

            if np.fabs(values - old_values).sum() < threshold:
                logger.info(f"\t\t· Done in {iteration} iterations")
                break

        self.q_function = q_function

    def run_policy_iteration(self, max_iterations: int = 200000, gamma: float = 1.0) -> None:
        """
        Estimates optimal policy function.

        Parameters
        ----------
        max_iterations: float
            Maximum number of iterations when looking for policy function.
        gamma: float
            Discount factor
        """
        logger.info("\t-  Starting policy iteration")
        num_states = len(self.environment.states)
        policy = np.zeros(num_states)
        optimal_value_function = np.zeros(num_states)

        for iteration in range(max_iterations):
            old_policy = policy.copy()
            optimal_value_function = self.evaluate_policy(policy)
            policy = self.improve_policy(optimal_value_function, gamma)

            if np.array_equal(policy, old_policy):
                logger.info(f"\t\t· Done in {iteration} iterations")
                break

        self.policy = policy
        self.state_value_function = optimal_value_function

    def evaluate_policy(self, policy: np.ndarray) -> np.ndarray:
        """
        Evaluates a policy (Q value for each cell).

        Parameters
        ----------
        policy: numpy.ndarray
            Policy to be evaluated using agents estimated Q function.

        Returns
        -------
        state_value_function: numpy.ndarray
        """

        value_function = np.zeros(self.environment.num_states)
        for state in range(self.environment.num_states):
            state = self.environment.get_state(state)
            action = policy[state.cell_id]

            value_function[state.cell_id] = self.q_function[state.cell_id][Action(action).value]

        return value_function

    def improve_policy(self, value_function, gamma) -> np.ndarray:
        """
        Computes a new policy for the given values.

        Parameters
        ----------
        value_function: numpy.ndarray
            Maximum Q values obtained with the curren policy
        gamma: float
            Discount factor

        Returns
        -------
        new_policy: numpy.ndarray
        """
        num_states = len(self.environment.states)
        policy = np.zeros(num_states)

        for state in range(num_states):
            best_q_function = None
            best_action = None
            state = self.environment.get_state(state)

            for action in state.actions:
                next_state_data = state.get_action_results(action)

                reward = next_state_data["transition_probability"] * (
                        next_state_data["reward"] + gamma * value_function[next_state_data["cell_id"]])

                if best_q_function is None or reward > best_q_function:
                    best_q_function = reward
                    best_action = action

            policy[state.cell_id] = best_action.value

        return policy

    def solve(self):
        """Solves the board using all estimated parameters."""

        player_positions = [self.environment.starting_position]
        reached_goal = False

        while not reached_goal:
            current_cell_id = player_positions[-1]
            next_action = Action(self.policy[current_cell_id])
            next_cell_data = self.environment.get_state(current_cell_id).actions[next_action]
            next_cell_state = self.environment.get_state(next_cell_data["cell_id"])

            if next_cell_state.cell_id in player_positions or next_cell_state.cell_type == -1:
                player_positions.append(next_cell_data["cell_id"])
                break

            player_positions.append(next_cell_data["cell_id"])
            reached_goal = next_cell_data["is_goal"]

        return player_positions, reached_goal

    def plot_q_function(self):
        """Polts a 3D density plot representing agent's Q function values distribution."""

        cells = np.arange(0, self.environment.num_states, 1)
        actions = np.arange(0, len(Action), 1)
        q_values = np.zeros((len(cells), len(actions)))

        for cell in cells:
            for action in actions:
                q_values[cell, action] = self.q_function[cell][action]

        q_values[q_values < 0] = -1 * (np.exp(q_values[q_values < 0]) - 1)

        fig = plt.figure(figsize=(13, 7))
        ax = plt.axes(projection='3d')
        surf = ax.plot_surface(np.expand_dims(cells, -1), np.expand_dims(actions, 0), q_values, rstride=1, cstride=1,
                               cmap='RdYlGn', edgecolor='none')
        ax.set_xlabel('CELL ID')
        ax.set_ylabel('ACTION')
        ax.set_zlabel('Q FUNCTION (SMOOTHED)')
        ax.set_title('TRAINING RESULTS')
        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.view_init(60, 35)
        plt.xticks(cells)
        plt.yticks(actions)
        plt.show()

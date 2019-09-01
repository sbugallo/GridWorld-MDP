import numpy as np
from loguru import logger

from .world import World
from .action import Action


class Agent:

    def __init__(self):
        self.policy: np.ndarray = np.array([])
        self.state_value_function: np.ndarray = np.array([])
        self.q_function: dict = {}
        self.environment: World = World()

    def train(self, world: World, policy_search_iterations: int = 200000, value_search_iterations: int = 100000,
              threshold: float = 1e-20, gamma: float = 0.99):

        logger.info("Beginning agent training")
        self.environment = world
        self.run_value_iteration(value_search_iterations, threshold, gamma)
        self.run_policy_iteration(policy_search_iterations, gamma)
        self.walk()

    def run_value_iteration(self, max_iterations: int = 100000, threshold: float = 1e-20,
                            gamma=0.99) -> None:

        logger.info("\tStarting value iteration")
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
                    q_values[action.name] = reward

                values[state.cell_id] = np.max(list(q_values.values()))
                q_function[state.cell_id] = q_values

            logger.info(f"\tValue iteration {iteration}: {np.fabs(values - old_values).sum()}")
            if np.fabs(values - old_values).sum() < threshold:
                break

        self.q_function = q_function

    def run_policy_iteration(self, max_iterations: int = 200000, gamma: float = 1.0) -> None:
        logger.info("\t-  Starting policy iteration")
        num_states = len(self.environment.states)
        policy = np.zeros(num_states)
        optimal_value_function = np.zeros(num_states)

        for iteration in range(max_iterations):
            old_policy = policy.copy()
            optimal_value_function = self.evaluate_policy(policy)
            policy = self.improve_policy(optimal_value_function, gamma)
            logger.info(f"\t\t · Policy iteration {iteration}: {policy}")
            if np.array_equal(policy, old_policy):
                break

        self.policy = policy
        self.state_value_function = optimal_value_function

    def evaluate_policy(self, policy):

        value_function = np.zeros(self.environment.num_states)
        for state in range(self.environment.num_states):
            state = self.environment.get_state(state)
            action = policy[state.cell_id]

            value_function[state.cell_id] = self.q_function[state.cell_id][Action(action).name]

        return value_function

    def improve_policy(self, value_function, gamma) -> np.ndarray:
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

    def walk(self):

        player_positions = [self.environment.starting_position]
        reached_goal = False

        while not reached_goal:
            current_cell_id = player_positions[-1]
            next_action = Action(self.policy[current_cell_id])
            next_cell_data = self.environment.get_state(current_cell_id).actions[next_action]

            if next_cell_data["cell_id"] in player_positions:
                break

            player_positions.append(next_cell_data["cell_id"])
            reached_goal = next_cell_data["is_goal"]

        self.environment.print(player_positions[1:-1])

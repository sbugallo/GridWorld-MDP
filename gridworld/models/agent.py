from pathlib import Path
import json

import numpy as np

from .action import Action


class Agent:

    def __init__(self):
        self.states = None
        self.policy = None
        self.transition_probabilities = None
        self.reward_probabilities = None
        self.state_value_function = None
        self.q_function = None
        self.current_state = None
        self.environment = None

    def get_next_move(self):
        return

    def run_value_iteration(self, max_iterations: int = 100000, threshold: float = 1e-20, gamma=1.0):
        num_states = len(self.environment)
        values = np.zeros(num_states)

        for iteration in range(max_iterations):
            new_values = values.copy()

            for state in range(num_states):
                q_value = []

                for action in Action:
                    rewards = []

                    for next_state in


    def serialize(self) -> dict:
        """
        Serializes this Agent as a dict.

        Returns
        -------
        serialized_agent: dict
        """

        return {
            "states": self.states,
            "policy": self.policy,
            "transition_probabilities": self.transition_probabilities,
            "reward_probabilities": self.reward_probabilities,
            "state_value_function": self.state_value_function,
            "q_function": self.q_function,
        }

    def deserialize(self, json_data):
        """
        Dumps specified `json_data` to the agent.

        Parameters
        ----------
        json_data: dict
            Dictionary with the following format: {mdp: dict}
        """

        self.states = json_data["states"]
        self.policy = json_data["policy"]
        self.transition_probabilities = json_data["transition_probabilities"]
        self.reward_probabilities = json_data["reward_probabilities"]
        self.state_value_function = json_data["state_value_function"]
        self.q_function = json_data["q_function"]

    def load(self, path: str) -> None:
        """
        Loads a JSON file containing agent's params.

        Parameters
        ----------
        path: str
            Path of the JSON file.
        """
        json_data = json.loads(Path(path).read_text())
        self.deserialize(json_data)

    def save(self, path: str) -> None:
        """
        Saves model's params as a JSON file.

        Parameters
        ----------
        path: str
            Where to save agent params.
        """
        with open(path, 'w') as fp:
            json.dump(self.serialize(), fp)
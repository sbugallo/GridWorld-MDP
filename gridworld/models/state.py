from .action import Action


class State:
    """
    Models states in a MDP.

    Attributes
    ----------
    cell_id: int
    cell_type: int
    actions: dict
        Format: {
            gridworld.models.Action: {
                "cell_id": int,
                "reward": gridworld.models.Reward,
                "transition_probability": float,
                "is_goal": bool
            }
        }
    """

    def __init__(self, cell_id: int, possible_moves: dict, cell_type: int) -> None:
        """
        Parameters
        ----------
        cell_id: int
            Cell index in world's grid.
        possible_moves: dict
            Format: {
                gridworld.models.Action: {
                    "cell_id": int,
                    "reward": gridworld.models.Reward,
                    "transition_probability": float,
                    "is_goal": bool
                }
            }
        cell_type: int
            0 -> road, 1 -> start, 2 -> goal, -1 -> obstacle
        """
        self.cell_id = cell_id
        self.cell_type = cell_type

        for move, next_state_data in possible_moves.items():
            if not isinstance(move, Action):
                raise ValueError("Move should be an Action instance")

            assert "cell_id" in next_state_data
            assert "reward" in next_state_data
            assert "is_goal" in next_state_data
            assert "transition_probability" in next_state_data

        self.actions = possible_moves

    def get_action_results(self, action: Action) -> dict:
        """
        Retrieves the results of performing specified `action` in current state.

        Parameters
        ----------
        action: gridworld.models.Action
            Action to be performed.

        Returns
        -------
        results: dict
            Format: {
                "cell_id": int,
                "reward": gridworld.models.Reward,
                "transition_probability": float,
                "is_goal": bool
            }
        """
        return self.actions[action]

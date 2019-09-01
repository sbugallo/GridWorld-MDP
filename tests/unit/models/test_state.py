import pytest

from gridworld.models import State, Reward, Action


@pytest.mark.unit
@pytest.mark.parametrize("cell_id, possible_moves, cell_type, reward", [
    (0,
     {
         Action.up: {
             "cell_id": 1,
             "reward": Reward.road,
             "transition_probability": 1.0,
             "is_goal": False
         }
     }, 0, Reward.road),
    (5,
     {
         Action.down:
             {
                 "cell_id": 4,
                 "reward": Reward.start,
                 "transition_probability": 1.0,
                 "is_goal": True
             }
     }, 1, Reward.start),
    (9,
     {
         Action.left:
             {
                 "cell_id": 3,
                 "reward": Reward.goal,
                 "transition_probability": 1.0,
                 "is_goal": False
             }
     }, 2, Reward.goal),
    (3,
     {
         Action.right:
             {
                 "cell_id": 17,
                 "reward": Reward.obstacle,
                 "transition_probability": 1.0,
                 "is_goal": True
             }
     }, -1,
     Reward.obstacle)
])
def test_state_correct_initialization(cell_id, possible_moves, cell_type, reward):
    state = State(cell_id, possible_moves, cell_type)

    assert state.cell_id == cell_id
    assert state.cell_type == cell_type
    assert state.reward == reward

    for move, next_state_data in state.actions.items():
        assert isinstance(move, Action)
        assert "cell_id" in next_state_data
        assert "reward" in next_state_data
        assert "transition_probability" in next_state_data
        assert "is_goal" in next_state_data


@pytest.mark.unit
def test_state_raises_error_if_possible_moves_keys_are_not_actions():
    with pytest.raises(ValueError, match="Move should be an Action instance"):
        State(2, {1: {}}, 0)


@pytest.mark.unit
@pytest.mark.parametrize("possible_moves", [
    {Action.up: {"cell_id": 2, "reward": 1, "transition_probability": 1.0}},
    {Action.up: {"cell_id": 3, "reward": 0, "is_goal": True}},
    {Action.up: {"cell_id": 4, "transition_probability": 0.5, "is_goal": False}},
    {Action.up: {"reward": -1, "transition_probability": 0.1, "is_goal": True}},
])
def test_state_raises_assertion_error_if_possible_moves_malformed(possible_moves):
    with pytest.raises(AssertionError):
        State(2, possible_moves, 0)

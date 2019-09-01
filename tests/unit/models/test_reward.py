import pytest

from gridworld.models import Reward


@pytest.mark.unit
def test_reward_correct_initialization():
    assert Reward(0) == Reward.start
    assert Reward(0) == Reward.road
    assert Reward(1) == Reward.goal
    assert Reward(-1) == Reward.obstacle


@pytest.mark.unit
def test_action_correct_values():
    assert Reward.start.value == 0
    assert Reward.road.value == 0
    assert Reward.goal.value == 1
    assert Reward.obstacle.value == -1

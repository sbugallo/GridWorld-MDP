import pytest

from gridworld.models import Action


@pytest.mark.unit
def test_action_correct_initialization():
    assert Action(0) == Action.up
    assert Action(1) == Action.down
    assert Action(2) == Action.right
    assert Action(3) == Action.left


@pytest.mark.unit
def test_action_correct_values():
    assert Action.up.value == 0
    assert Action.down.value == 1
    assert Action.right.value == 2
    assert Action.left.value == 3

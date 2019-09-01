from gridworld.models import Game, World, Agent

import pytest
from numpy.testing import assert_array_equal
import numpy as np


@pytest.mark.unit
def test_game_initializes_correctly():

    game = Game(4, 4, 0, 15, [5, 7, 11, 12])

    assert isinstance(game.world, World)
    assert game.world.num_states == 16
    assert game.world.grid_height == 4
    assert game.world.grid_width == 4
    assert game.world.starting_position == 0
    assert game.world.goal_position == 15
    assert game.world.obstacle_positions == [5, 7, 11, 12]
    assert_array_equal(game.world.grid, np.array([1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, -1, 0, 0, 2]))

    assert isinstance(game.agent, Agent)
    assert_array_equal(game.agent.policy, [])
    assert_array_equal(game.agent.state_value_function, [])
    assert not game.agent.q_function
    assert isinstance(game.agent.environment, World)


@pytest.mark.unit
def test_game_play_expected_result(mocker):

    with mocker.patch('matplotlib.pyplot.show',):
        player_positions, reached_goal = Game(4, 4, 0, 15, [5, 7, 11, 12]).play()

        assert reached_goal is True
        assert player_positions == [0, 4, 8, 9, 13, 14, 15]


@pytest.mark.unit
def test_game_play_expected_result_with_impossible_game(mocker):

    with mocker.patch('matplotlib.pyplot.show',):
        player_positions, reached_goal = Game(4, 4, 0, 15, [1, 4]).play()

        assert reached_goal is False
        assert player_positions == [0, 0]

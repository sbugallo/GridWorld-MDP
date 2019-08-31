import pytest
from numpy.testing import assert_array_equal

from gridworld.models import World


@pytest.mark.unit
def test_world_default_initialization():
    world = World()

    assert world.grid_width == 4
    assert world.grid_height == 4
    assert world.starting_position == 0
    assert world.goal_position == 15
    assert world.obstacle_positions == [5, 7, 11, 12]
    assert_array_equal(world.grid, [1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, -1, 0, 0, 2])


@pytest.mark.unit
@pytest.mark.parametrize("height, width, start, end, obstacles, player_positions, result", [
    (2, 1, 0, 1, [], None, ['\x1b[42m', '\x1b[44m']),
    (3, 3, 0, 8, [], [], ['\x1b[42m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m',
                          '\x1b[44m']),
    (3, 3, 0, 8, [1, 2, 3, 4, 5, 6, 7], [], ['\x1b[42m', '\x1b[41m', '\x1b[41m', '\x1b[41m', '\x1b[41m', '\x1b[41m',
                                             '\x1b[41m', '\x1b[41m', '\x1b[44m']),
    (5, 3, 0, 1, [], [], ['\x1b[42m', '\x1b[44m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m',
                          '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m', '\x1b[47m',
                          '\x1b[47m']),
    (4, 4, 0, 15, [5, 7, 11, 12], [1, 2, 6, 10, 14], ['\x1b[42m', '\x1b[46m', '\x1b[46m', '\x1b[47m', '\x1b[47m',
                                                      '\x1b[41m', '\x1b[46m', '\x1b[41m', '\x1b[47m', '\x1b[47m',
                                                      '\x1b[46m', '\x1b[41m', '\x1b[41m', '\x1b[47m', '\x1b[46m',
                                                      '\x1b[44m'])
])
def test_world_generates_correct_grid(height, width, start, end, obstacles, player_positions, result):

    world = World(grid_width=width, grid_height=height, starting_position=start, goal_position=end,
                  obstacle_positions=obstacles)

    assert world.print(player_positions) == result


@pytest.mark.unit
def test_world_raises_value_error_if_incompatible_start_positions():
    with pytest.raises(ValueError, match="Starting cell -1 is not valid"):
        World(starting_position=-1)


@pytest.mark.unit
@pytest.mark.parametrize("goal", [0, -1])
def test_world_raises_value_error_if_incompatible_goal_positions(goal):
    with pytest.raises(ValueError, match=f"Goal cell {goal} is not valid"):
        World(goal_position=goal)


@pytest.mark.unit
@pytest.mark.parametrize("obstacles", [[0], [-1], [15]])
def test_world_raises_value_error_if_incompatible_obstacles_positions(obstacles):
    with pytest.raises(ValueError, match=f"Obstacle cell {obstacles[0]} is not valid"):
        World(obstacle_positions=obstacles)
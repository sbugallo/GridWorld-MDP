import numpy as np
import pytest
from numpy.testing import assert_array_equal

from gridworld.models import Agent, World


@pytest.mark.unit
def test_agent_initialization():
    agent = Agent()

    assert isinstance(agent, Agent)
    assert_array_equal(agent.policy, [])
    assert_array_equal(agent.state_value_function, [])
    assert not agent.q_function
    assert isinstance(agent.environment, World)


@pytest.mark.unit
def test_agent_run_value_iteration_expected_results():
    agent = Agent()

    agent.run_value_iteration(max_iterations=1)
    assert agent.q_function == {0: {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0},
                                1: {0: 0.0, 1: -16.0, 2: 0.0, 3: 0.0},
                                2: {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0},
                                3: {0: 0.0, 1: -16.0, 2: 0.0, 3: 0.0},
                                4: {0: 0.0, 1: 0.0, 2: -16.0, 3: 0.0},
                                5: {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0},
                                6: {0: 0.0, 1: 0.0, 2: -16.0, 3: -16.0},
                                7: {0: 0.0, 1: -16.0, 2: -16.0, 3: 0.0},
                                8: {0: 0.0, 1: -16.0, 2: 0.0, 3: 0.0},
                                9: {0: -16.0, 1: 0.0, 2: 0.0, 3: 0.0},
                                10: {0: 0.0, 1: 0.0, 2: -16.0, 3: 0.0},
                                11: {0: -16.0, 1: 1.0, 2: -16.0, 3: 0.0},
                                12: {0: 0.0, 1: -16.0, 2: 0.0, 3: -16.0},
                                13: {0: 0.0, 1: 0.0, 2: 0.0, 3: -16.0},
                                14: {0: 0.0, 1: 0.0, 2: 1.0, 3: 0.0},
                                15: {0: -16.0, 1: 1.0, 2: 1.0, 3: 0.0}}


@pytest.mark.unit
def test_agent_run_policy_iteration_expected_results():
    agent = Agent()
    agent.run_value_iteration(max_iterations=1)
    agent.run_policy_iteration(max_iterations=1)

    assert_array_equal(agent.policy, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 3])
    assert_array_equal(agent.state_value_function, [0, 0, 0, 0, 0, 0, 0, 0, 0, -16, 0, -16, 0, 0, 0, -16])


@pytest.mark.unit
def test_agent_evaluate_policy_expected_results():
    policy = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 3])
    agent = Agent()
    agent.run_value_iteration(max_iterations=1)
    assert_array_equal(agent.evaluate_policy(policy), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


@pytest.mark.unit
def test_agent_improve_policy_expected_results():
    value_function = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    agent = Agent()
    agent.run_value_iteration(max_iterations=1)

    assert_array_equal(agent.improve_policy(value_function, 1.), [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 1])


def test_agent_solve_expected_results():
    agent = Agent()
    agent.run_value_iteration()
    agent.run_policy_iteration()

    player_positions, reached_goal = agent.solve()
    assert reached_goal is True
    assert player_positions == [0, 4, 8, 9, 13, 14, 15]

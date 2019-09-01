Play game
=========

To play a game simply run the following command:

.. code:: bash

    gridworld-play

If you want to use your own configuration, run:

.. code:: bash

    gridworld-play \
    --world_width <World's width in cells. | int> \
    --world_height <World's height in cells. | int> \
    --start_cell <Cell where the agent will start. | int> \
    --goal_cell <Cell where the agent has to go. | int> \
    --obstacles_cells <Cells where obstacles will be placed. | list> \
    --policy_search_iterations <Maximum number of iterations when looking for optimal policy. | int> \
    --value_search_iterations <Maximum number of iterations when looking for optimal state-value function. | int> \
    --threshold <Minimum change that should happen to continue value search iteration. | float> \
    --gamma <Discount factor | float>

Example:

.. code:: bash

    gridworld-play \
    --world_width 4 \
    --world_height 4 \
    --start_cell 0 \
    --goal_cell 15 \
    --obstacles_cells [5,7,11,12] \
    --policy_search_iterations 100000 \
    --value_search_iterations 20000 \
    --threshold 0.8 \
    --gamma 0.99
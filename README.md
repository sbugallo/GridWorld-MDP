# Grid World AI - Markov Decision Process

[![CodeFactor](https://www.codefactor.io/repository/github/sbugallo/gridworld-mdp/badge)](https://www.codefactor.io/repository/github/sbugallo/gridworld-mdp)
[![Build Status](https://travis-ci.com/sbugallo/GridWorld-MDP.svg)](https://travis-ci.com/sbugallo/GridWorld-MDP)
[![Coverage Status](https://coveralls.io/repos/github/sbugallo/GridWorld-MDP/badge.svg?branch=master)](https://coveralls.io/github/sbugallo/GridWorld-MDP?branch=master)

<img src="https://raw.githubusercontent.com/sbugallo/GridWorld-MDP/master/docs/_static/logo-color.png" width="50%" />

## Game description

<div style="display: flex;">
    <img src="https://raw.githubusercontent.com/sbugallo/GridWorld-MDP/master/docs/_static/game.gif" width="30%"/> <img src="https://raw.githubusercontent.com/sbugallo/GridWorld-MDP/master/docs/_static/q_function.JPG" width="55%"/> 
</div>

The agent lives in a grid. Our agent must go from the starting cell (green square) to the goal cell (blue cell) but 
there are some obstacles (red squares) blocking the agent’s path. 

## Installation usage

See [documentation](https://sbugallo.github.io/GridWorld-MDP/).

A docker image is available at 
[https://hub.docker.com/r/sbugallo/gridworld](https://hub.docker.com/r/sbugallo/gridworld). Simply run 
`docker run -ti sbugallo/gridworld` and then 

```bash
gridworld-play
```
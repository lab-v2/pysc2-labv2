# pysc2-labv2
Our implementation of PySC2 on Windows.

## Structure
`pr-qtable.npy` is the qlearning based learnt policy file using PyReason. It can be used to play the game.

`Base_Map_no_attack.SC2Map` is the current map being used for the game: no shooting, only movement. It is created using the SC2 map editor.

The files `interface_marine.py` is the main file which creates an instance of pySC2 game and then runs our RL based policy for 10 episodes. The `interface_marine.py` uses the `step_update.py` file which contains wrapper functions to interface with pySC2 game as a grid world and also load the learned policy stored as a Q-table in `pr-qtable.npy`.

# pysc2-labv2
Our implementation of PySC2

## Structure
The files `interface_marine.py` is the main file which creates an instance of pySC2 game and then runs our RL based policy for 10 episodes. The `interface_marine.py` uses the `step_update.py` file which contains wrapper functions to interface with pySC2 game as a grid world and also load the learned policy stored as a Q-table in `non-pr-qtable-15000.npy` file.

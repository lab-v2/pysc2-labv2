# pysc2-labv2
Our implementation of PySC2

Only marine movement:
Map:

The map "Base_Map_no_attack.SC2Map" features a landscape with mountains, a red base, and a blue base. Each team possesses five marines, constrained to navigating around the mountains rather than crossing them. The primary objective is for one team to achieve victory by having any of their marines enter the opposing team's base. Movement options for the marines include remaining stationary or moving in any of the four cardinal directions. Feel free to adjust the number of marines to meet specific requirements within the map.

Files:

custom.py
n_marine_interface.py
interface_step_update.py
memo.py

marine + Tank movement:

Map:

The map "Base_Map.SC2Map" features a landscape with mountains, a red base, and a blue base. Each team possesses 2 marines and tank each, constrained to navigating around the mountains rather than crossing them. Movement options for the marines and tanks include remaining stationary or moving in any of the four cardinal directions. The number of tanks and marines are fixed for the implementation sake.

Files:

multiunit_runtime_tank.py




# pysc2-labv2
Our implementation of PySC2

## Environment:

PySC2 is a learning environment of StarCraft II. It provides a way to interact with StarCraft II by getting observations and taking actions. For Installation follow [PySC2 - StarCraft II Learning Environment](https://github.com/deepmind/pysc2)

## Only marine movement:
**Map**:

The map "Base_Map_no_attack.SC2Map" features a landscape with mountains, a red base, and a blue base. Each team possesses five marines, constrained to navigating around the mountains rather than crossing them. The primary objective is for one team to achieve victory by having any of their marines enter the opposing team's base. Movement options for the marines include remaining stationary or moving in any of the four cardinal directions. Feel free to adjust the number of marines to meet specific requirements within the map.

**Files**:

* custom.py : The changes to this file has to be made to include the new maps, for reference "Base_Map.SC2Map" has been added. you can find the file under maps folder. Path would be Python\Python310\Lib\site-packages\pysc2\maps.
* n_marine_interface.py : This file is used to get the map, model and initialize all the marines and waits for the actions from the "interface_step_update.py" file. Then moves according to the corresponding actions. Each game runs for a certain number of times specified by "Episodes". The policies for the model are taken from a certain folder, which is mentioned in the "memo.py" file. All the essential parameters such as time, memory, the number of steps and the rewards are tracked in seperate files.
* interface_step_update.py : This file has two important parts, blue team movement is random and all the marines are assigned a directions randomly. On the other hand, the red movement takes the marine tags from "n_marine_interface.py" and calculates the next step a marine should take based on the location of the enemies and creates an action with new location of the active marine. Rewards are also calculated accordingly and returned along with the actions.
* memo.py : The file is used to run the program with multiple policies mentioned in the zip files.

## marine + tank movement:

**Map**:

The map "Base_Map.SC2Map" features a landscape with mountains, a red base, and a blue base. Each team possesses 2 marines and tank each, constrained to navigating around the mountains rather than crossing them. Movement options for the marines and tanks include remaining stationary or moving in any of the four cardinal directions. The number of tanks and marines are fixed for the implementation sake.

**Files**:

multiunit_runtime_tank.py : This file serves the purpose of directing the movements of marines and tanks based on user-provided actions. It represents a fundamental implementation approach.




from pysc2.maps import lib


class Custom(lib.Map):
  filename = "Base_Map"
  directory = ""
  download = "C:/Program Files (x86)/StarCraft II/Maps/Test/"
  players = 2
  game_steps_per_episode = 16 * 60 * 3  # 3 minute limit.


cus_maps = [
    # "Empty128",  # Not really playable, but may be useful in the future.
    "Map1",
    "Base_Map",
    "Base1",
    "Base_Map_no_attack"
]

for name in cus_maps:
  globals()[name] = type(name, (Custom,), dict(filename=name))
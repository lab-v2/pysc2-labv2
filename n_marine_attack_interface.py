from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
from pysc2.maps import lib
import random
from pysc2.env.environment import TimeStep
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import sys
import tracemalloc
import interface_step_update_attack

num_of_soldiers=interface_step_update_attack.total_number_of_soldiers()
map_name="Base_Map_attack"

class TerranAgent(base_agent.BaseAgent):
    def __init__(self):
        super(TerranAgent, self).__init__()
        self.attack_coordinates = None
        for i in range(1, num_of_soldiers + 1):
            setattr(self, f"marine_tag{i}", None)
        self.tank_tag = None
        self.num_step = 0

    def unit_type_is_selected(self, obs, unit_type):
        if (
            len(obs.observation.single_select) > 0
            and obs.observation.single_select[0].unit_type == unit_type
        ):
            return True

        if (
            len(obs.observation.multi_select) > 0
            and obs.observation.multi_select[0].unit_type == unit_type
        ):
            return True

        return False

    def get_units_by_type(self, obs, unit_type):
        return [
            unit
            for unit in obs.observation.feature_units
            if unit.unit_type == unit_type
        ]

    @staticmethod
    def get_raw_units_by_type(obs, unit_type):
        return [
            unit for unit in obs.observation.raw_units if unit.unit_type == unit_type
        ]

    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    def update_marine_tags(self, marines):
        for i, marine in enumerate(marines):
            if i == 0:
                if self.marine_tag1 is None:
                    self.marine_tag1 = marine.tag
            else:
                prev_tags = [
                    getattr(self, f"marine_tag{i}") for i in range(1, num_of_soldiers + 1)
                ]

                if marine.tag not in prev_tags:
                    for j in range(len(prev_tags)):
                        if prev_tags[j] is None:
                            setattr(self, f"marine_tag{j+1}", marine.tag)
                            break

    def get_selected_marines(self):
        selected_marines = []
        for i in range(1, num_of_soldiers + 1):
            marine_tag = getattr(self, f"marine_tag{i}")
            if marine_tag:
                selected_marines.append(marine_tag)
        return selected_marines

    def step(self, obs):
        super(TerranAgent, self).step(obs)
        marine = []
        xcor = []
        ycor = []
        unit_actions = []
        unit_tags = []
        self.num_step += 1
        marines = self.get_raw_units_by_type(obs, units.Terran.Marine)

        self.update_marine_tags(marines)

        unit_tags = self.get_selected_marines()
        marine = [unit for unit in marines if unit.tag in unit_tags]

        length = len(unit_tags)
        if isinstance(self, TerranAgent1):
            unit_actions = interface_step_update_attack.redSteps(
                self.num_step, unit_tags, marine, xcor, ycor, length
            )
        elif isinstance(self, TerranAgent2):
            unit_actions = interface_step_update_attack.blueSteps(
                self.num_step, unit_tags, marine, xcor, ycor, length
            )

        self.num_step += 1
        return unit_actions


class TerranAgent1(TerranAgent):
    def __init__(self):
        super(TerranAgent1, self).__init__()

    def step(self, obs):
        return super(TerranAgent1, self).step(obs)


class TerranAgent2(TerranAgent):
    def __init__(self):
        super(TerranAgent2, self).__init__()

    def step(self, obs):
        return super(TerranAgent2, self).step(obs)




def main(unused_argv):
    tracemalloc.start()
    agent1 = TerranAgent1()
    agent2 = TerranAgent2()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name = map_name,
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Agent(sc2_env.Race.terran)],
                agent_interface_format = features.AgentInterfaceFormat(
                    feature_dimensions = features.Dimensions(screen=84, minimap=64),
                    use_feature_units = True,
                    use_raw_units = True,
                    use_raw_actions=True,
                    rgb_dimensions=sc2_env.Dimensions(screen=256,minimap=256)
                ),
                step_mul = 100,
                game_steps_per_episode = 0,
                visualize=True
            ) as env:
                
                agent1.setup(env.observation_spec(), env.action_spec())
                agent2.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent1.reset()
                agent2.reset()
                step_num = 0
                while True:
                    step_actions = [agent1.step(timesteps[0]), agent2.step(timesteps[1])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)
                    step_num=step_num+1
                    print("step num : ",step_num)
                    if(step_num==100):
                        mem = tracemalloc.get_traced_memory()[1]/(10**6) 
                        print('Program used:', mem, 'MB of memory')
                        sys.exit()
    except KeyboardInterrupt:
        mem = tracemalloc.get_traced_memory()[1]/(10**6) 
        print('Program used:', mem, 'MB of memory') 
        tracemalloc.stop()
        pass


if __name__ == "__main__":
    app.run(main)
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

class TerranAgent1(base_agent.BaseAgent):
    def __init__(self):
        super(TerranAgent1, self).__init__()
        self.attack_coordinates = None
        for i in range(1, 11):
            setattr(self, f"marine_tag{i}", None)

        self.tank_tag = None
        self.num_step = 0

    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    # def get_raw_units_by_type(self, obs, unit_type):
    #     return [unit for unit in obs.observation.raw_units if unit.unit_type == unit_type]
    @staticmethod
    def get_raw_units_by_type(obs: TimeStep, unit_type):
        return [unit for unit in obs.observation.raw_units if unit.unit_type == unit_type]
    
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    
    def step(self, obs):
        super(TerranAgent1, self).step(obs)
        self.num_step+=1
        marines = self.get_raw_units_by_type(obs, units.Terran.Marine)
        #Tanks = self.get_raw_units_by_type(obs, units.Terran.SiegeTank)
        # if(self.tank_tag==None):
        #     self.tank_tag = Tanks[0].tag
        for i, marine in enumerate(marines):
            if i == 0:
                if self.marine_tag1 is None:
                    self.marine_tag1 = marine.tag
            else:
                prev_tags = [self.marine_tag1, self.marine_tag2, self.marine_tag3, self.marine_tag4, self.marine_tag5, self.marine_tag6, self.marine_tag7, self.marine_tag8, self.marine_tag9, self.marine_tag10]
                if marine.tag not in prev_tags:
                    for j in range(len(prev_tags)):
                        if prev_tags[j] is None:
                            setattr(self, f"marine_tag{j+1}", marine.tag)
                            break     
        marine = []
        xcor=[]
        ycor=[]
        unit_actions = []
        unit_tags = []
        for i in range(1, len(prev_tags)+1):
            marine_tag = getattr(self, f"marine_tag{i}")
            unit_tags.append(marine_tag)

        marine = []
        for i in range(1, len(prev_tags)+1):
            marine_tag = getattr(self, f"marine_tag{i}")
            if marine_tag:
                marine.append([unit for unit in marines if unit.tag == marine_tag][0])
        #marine.append([unit for unit in Tanks if unit.tag == self.tank_tag][0])
        length=len(prev_tags)
        unit_actions = interface_step_update_attack.my_methodR(self.num_step, unit_tags, marine, xcor, ycor, length) 
        self.num_step+=1    
        return unit_actions   

class TerranAgent2(base_agent.BaseAgent):

    def __init__(self):
        super(TerranAgent2, self).__init__()
        self.attack_coordinates = None
        for i in range(1, 11):
            setattr(self, f"marine_tag{i}", None)

        self.tank_tag = None
        self.num_step = 0

    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    # def get_raw_units_by_type(self, obs, unit_type):
    #     return [unit for unit in obs.observation.raw_units if unit.unit_type == unit_type]
    @staticmethod
    def get_raw_units_by_type(obs: TimeStep, unit_type):
        return [unit for unit in obs.observation.raw_units if unit.unit_type == unit_type]
    
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    
    def step(self, obs):
        super(TerranAgent2, self).step(obs)
        self.num_step+=1
        marines = self.get_raw_units_by_type(obs, units.Terran.Marine)
        #Tanks = self.get_raw_units_by_type(obs, units.Terran.SiegeTank)
        # if(self.tank_tag==None):
        #     self.tank_tag = Tanks[0].tag
        for i, marine in enumerate(marines):
            if i == 0:
                if self.marine_tag1 is None:
                    self.marine_tag1 = marine.tag
            else:
                prev_tags = [self.marine_tag1, self.marine_tag2, self.marine_tag3, self.marine_tag4, self.marine_tag5, self.marine_tag6, self.marine_tag7, self.marine_tag8, self.marine_tag9, self.marine_tag10]
                if marine.tag not in prev_tags:
                    for j in range(len(prev_tags)):
                        if prev_tags[j] is None:
                            setattr(self, f"marine_tag{j+1}", marine.tag)
                            break           
        marine = []
        xcor=[]
        ycor=[]
        unit_actions = []
        unit_tags = []
        for i in range(1, len(prev_tags)+1):
            marine_tag = getattr(self, f"marine_tag{i}")
            unit_tags.append(marine_tag)

        marine = []
        for i in range(1, len(prev_tags)+1):
            marine_tag = getattr(self, f"marine_tag{i}")
            if marine_tag:
                marine.append([unit for unit in marines if unit.tag == marine_tag][0])

        #marine.append([unit for unit in Tanks if unit.tag == self.tank_tag][0])
        length=len(prev_tags)
        unit_actions = interface_step_update_attack.my_methodB(self.num_step, unit_tags, marine, xcor, ycor, length) 
        self.num_step+=1    
        return unit_actions



def main(unused_argv):
    tracemalloc.start()
    agent1 = TerranAgent1()
    agent2 = TerranAgent2()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name ="Base_Map_attack",
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
                    # im=Image.fromarray(timesteps[0].observation.rgb_minimap.astype(np.uint8))
                    # im.save("minimap.jpeg")
                    # im1=Image.fromarray(timesteps[0].observation.rgb_minimap.astype(np.uint8))
                    # im1.save(f"agent1step_{step_num}.png")
                    # im2=Image.fromarray(timesteps[1].observation.rgb_minimap.astype(np.uint8))
                    # im2.save(f"agebt2step_{step_num}.png")
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
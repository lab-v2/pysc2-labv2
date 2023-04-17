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


class TerranAgent1(base_agent.BaseAgent):

    r_str = sys.argv[1]
    b_str = sys.argv[2]


    # Define up and down as strings
    up = "up"
    down = "down"
    nop = "nop"
    right = "right"
    left = "left"


    # convert the two strings into lists
    R = eval(r_str)
    B = eval(b_str)
    # R=[["up","nop"],["up","nop"]]
    # B=[["right","down"],["right","down"]]
    def __init__(self):
        super(TerranAgent1, self).__init__()
        self.attack_coordinates = None
        self.marine_tag1 = None
        self.marine_tag2 = None
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
        if(len(self.R) <= self.num_step):
            return actions.RAW_FUNCTIONS.no_op()
        agent_step = self.R[self.num_step]
        self.num_step+=1
        marines = self.get_raw_units_by_type(obs, units.Terran.Marine)
        Tanks = self.get_raw_units_by_type(obs, units.Terran.SiegeTank)
        if(self.tank_tag==None):
            self.tank_tag = Tanks[0].tag
        if(self.marine_tag1==None):
            self.marine_tag1=marines[0].tag
        if(self.marine_tag2==None and marines[1].tag!=self.marine_tag1):
            self.marine_tag2=marines[1].tag
        marine = []
        xcor=[]
        ycor=[]
        unit_actions = []
        unit_tags = [self.marine_tag1, self.marine_tag2, self.tank_tag]
        marine.append([unit for unit in marines if unit.tag == self.marine_tag1][0])
        marine.append([unit for unit in marines if unit.tag == self.marine_tag2][0])
        marine.append([unit for unit in Tanks if unit.tag == self.tank_tag][0])
        for i in range(3):     
            ycor.append(marine[i].y)
            xcor.append(marine[i].x)
            if(agent_step[i]=="up"):
                ycor[i]=int(ycor[i])-10
            if(agent_step[i]=="down"):
                ycor[i]=int(ycor[i])+10
            if(agent_step[i]=="left"):
                xcor[i]=int(xcor[i])-10
            if(agent_step[i]=="right"):
                xcor[i]=int(xcor[i])+10                        
            unit_actions.append(actions.RAW_FUNCTIONS.Attack_pt("now", unit_tags[i], (xcor[i],ycor[i])))
        return unit_actions    

class TerranAgent2(base_agent.BaseAgent):

    r_str = sys.argv[1]
    b_str = sys.argv[2]


    # Define up and down as strings
    up = "up"
    down = "down"
    nop = "nop"
    right = "right"
    left = "left"


    # convert the two strings into lists
    R = eval(r_str)
    B = eval(b_str)
    # R=[["up","nop"],["up","nop"]]
    # B=[["right","down"],["right","down"]]

    def __init__(self):
        super(TerranAgent2, self).__init__()
        self.attack_coordinates = None
        self.marine_tag3 = None
        self.marine_tag4 = None
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
        if(len(self.B) <= self.num_step):
            return actions.RAW_FUNCTIONS.no_op()
        agent_step = self.B[self.num_step]
        self.num_step+=1
        marines = self.get_raw_units_by_type(obs, units.Terran.Marine)
        Tanks = self.get_raw_units_by_type(obs, units.Terran.SiegeTank)
        if(self.tank_tag==None):
            self.tank_tag = Tanks[0].tag
        if(self.marine_tag3==None):
            self.marine_tag3=marines[0].tag
        if(self.marine_tag4==None and marines[1].tag!=self.marine_tag3):
            self.marine_tag4=marines[1].tag
        marine = []
        xcor=[]
        ycor=[]
        unit_actions = []
        unit_tags = [self.marine_tag3, self.marine_tag4, self.tank_tag]
        marine.append([unit for unit in marines if unit.tag == self.marine_tag3][0])
        marine.append([unit for unit in marines if unit.tag == self.marine_tag4][0])
        marine.append([unit for unit in Tanks if unit.tag == self.tank_tag][0])
        for i in range(3):     
            ycor.append(marine[i].y)
            xcor.append(marine[i].x)   
            if(agent_step[i]=="up"):
                ycor[i]=int(ycor[i])+10
            if(agent_step[i]=="down"):
                ycor[i]=int(ycor[i])-10
            if(agent_step[i]=="left"):
                xcor[i]=int(xcor[i])-10
            if(agent_step[i]=="right"):
                xcor[i]=int(xcor[i])+10
            #result = step_update.my_method(my_list1, my_list2)                       
            unit_actions.append(actions.RAW_FUNCTIONS.Attack_pt("now", unit_tags[i], (xcor[i],ycor[i])))

        return unit_actions



def main(unused_argv):
    agent1 = TerranAgent1()
    agent2 = TerranAgent2()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name ="Base_Map",
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
                    im1=Image.fromarray(timesteps[0].observation.rgb_minimap.astype(np.uint8))
                    im1.save(f"agent1step_{step_num}.png")
                    im2=Image.fromarray(timesteps[1].observation.rgb_minimap.astype(np.uint8))
                    im2.save(f"agebt2step_{step_num}.png")
                    step_actions = [agent1.step(timesteps[0]), agent2.step(timesteps[1])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)
                    step_num=step_num+1
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app.run(main)

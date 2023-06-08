from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
from pysc2.maps import lib
import pysc2
from pysc2.env.environment import TimeStep
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import sys
import step_update as step_update_interface
from pysc2.maps import *
from pysc2.lib import point
import time
import observ

file1Name = 'fileEach15000_times.txt'
file2Name = 'file15000.txt'

## Red Agent (Our Agent)
class TerranAgent1(base_agent.BaseAgent):

    def __init__(self):
        super(TerranAgent1, self).__init__()
        self.attack_coordinates = None
        self.marine_tag1 = None
        # self.marine_tag2 = None
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
    
    def get_enemy_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.raw_units
            if unit.unit_type == unit_type
            and unit.alliance == features.PlayerRelative.ENEMY]

    @staticmethod
    def get_raw_units_by_type(obs: TimeStep, unit_type):
        return [unit for unit in obs.observation.raw_units if unit.unit_type == unit_type]
    
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    
    def step(self, obs, blue_pos):
        super(TerranAgent1, self).step(obs)
        marines = self.get_raw_units_by_type(obs, units.Terran.Marine)

        if(self.marine_tag1==None):
            self.marine_tag1=marines[0].tag
        marine = []
        xcor=[]
        ycor=[]
        unit_actions = []
        unit_tags = [self.marine_tag1]
        marine.append([unit for unit in marines if unit.tag == self.marine_tag1][0])
        unit_actions, done, reward = step_update_interface.my_methodR(self.num_step, unit_tags, marine, xcor, ycor, blue_pos) 
        self.num_step+=1    
        return unit_actions, done, reward


## Blue Agent (Opponent)
class TerranAgent2(base_agent.BaseAgent):

    def __init__(self):
        super(TerranAgent2, self).__init__()
        self.attack_coordinates = None
        self.marine_tag3 = None
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

    @staticmethod
    def get_raw_units_by_type(obs: TimeStep, unit_type):
        return [unit for unit in obs.observation.raw_units if unit.unit_type == unit_type]
    
    def can_do(self, obs, action):
        return action in obs.observation.available_actions
    
    
    def step(self, obs):
        super(TerranAgent2, self).step(obs)
        marines = self.get_raw_units_by_type(obs, units.Terran.Marine)
        if(self.marine_tag3==None):
            self.marine_tag3=marines[0].tag
        marine = []
        xcor=[]
        ycor=[]
        unit_actions = []
        unit_tags = [self.marine_tag3]
        marine.append([unit for unit in marines if unit.tag == self.marine_tag3][0])
        unit_actions, pos, done, reward = step_update_interface.my_methodB(self.num_step, unit_tags, marine, xcor, ycor) 
        self.num_step+=1
        return unit_actions, pos, done, reward



def main(unused_argv):

    agent1 = TerranAgent1()
    agent2 = TerranAgent2()
    observ.printloc()
    winner_blue_cnt = 0
    winner_red_cnt = 0
    print("Starting 5 Run experiment")
    try:
        with sc2_env.SC2Env(
            map_name ="Base_Map_no_attack",
            players=[sc2_env.Agent(sc2_env.Race.terran),
                     sc2_env.Agent(sc2_env.Race.terran)],
            agent_interface_format = features.AgentInterfaceFormat(
                feature_dimensions = features.Dimensions(screen=84, minimap=64),
                use_feature_units = True,
                use_raw_units = True,
                use_raw_actions=True,
                # rgb_dimensions=None
                rgb_dimensions=sc2_env.Dimensions(screen=256,minimap=256)
            ),
            # score_index=0,
            step_mul = 100,
            game_steps_per_episode = 0,
            visualize=True
            # visualize=False
        ) as env:
            agent1.setup(env.observation_spec(), env.action_spec())
            agent2.setup(env.observation_spec(), env.action_spec())
            with open(file1Name, 'a') as ff:
                ff.write("Trials with Visualization + Prints + Rewards" + '\n')
            for tt in range(10):
                start = time.time()
                timesteps = env.reset()
                agent1.reset()
                agent2.reset()
                step_num = 0
                ep_reward = 0
                pos = (30, 28)
                while True:
                    agent1_actions, doneR, reward1 = agent1.step(timesteps[0], pos)
                    agent2_actions, pos, doneB, reward2 = agent2.step(timesteps[1])
                    step_actions = [agent1_actions, agent2_actions]
                    ep_reward += (reward1 + reward2)
                    ## If red agent reaches the blue base stop
                    if doneR:
                        winner_red_cnt += 1
                        with open(file1Name, 'a') as ff:
                            ff.write("Trial " + str(tt) + " Winner: Red" + '\t')
                        break
                    if doneB:
                        winner_blue_cnt += 1
                        with open(file1Name, 'a') as ff:
                            ff.write("Trial " + str(tt) + " Winner: Blue" + '\t')
                        break
                    
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)
                    step_num=step_num+1
                with open(file1Name, 'a') as ff:
                    ff.write("Time:" + str(time.time() - start) + "\t")
                    ff.write("Total Reward:" + str(ep_reward) + "\n")
        line = "Win Percentage:"+ str(winner_red_cnt)
        with open(file2Name, 'w') as f:
            f.write(line + '\n')
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app.run(main)
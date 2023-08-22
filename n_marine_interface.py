from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
from pysc2.maps import lib
import pysc2
from pysc2.env.environment import TimeStep
import sys
import interface_step_update as step_update_interface
from pysc2.maps import *
from pysc2.lib import point
import time
import tracemalloc
from torch import nn
import torch

file1Name = 'C:/Users/lahar/Downloads/experiment/Policy5stats.txt' #path to file with wins for each game
file2Name = 'C:/Users/lahar/Downloads/experiment/Policy5wins.txt' #path to file with all the details for each policy

map_name = "Base_Map_no_attack"

num_agents=5
# directions a marine can take
directions = ['up', 'down', 'left', 'right', 'nop']

class Network(nn.Module):
    def __init__(self) -> None:
        super().__init__()

        in_features = (num_agents+1)*2

        self.net = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.Tanh(),
            nn.Linear(64, len(directions))
        )
    
    def forward(self, x):
        return self.net(x)
    
    def act(self, obs):
        obs_t = torch.as_tensor(obs, dtype=torch.float32)
        q_values = self(obs_t.unsqueeze(0))

        max_q_index = torch.argmax(q_values, dim=1)[0]
        action = max_q_index.detach().item()

        return action

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

## Red Agent (Our Agent)
class TerranAgent1(base_agent.BaseAgent):

    def __init__(self):
        super(TerranAgent1, self).__init__()
        self.attack_coordinates = None
        for i in range(1, num_agents+1):
            setattr(self, f"marine_tag{i}", None)
        self.tank_tag = None
        self.num_step = 0
    
    def step(self, obs, blue_pos, player_net):
        super(TerranAgent1, self).step(obs)
        marines = get_raw_units_by_type(obs, units.Terran.Marine)

        # initializing marine tags
        for i, marine in enumerate(marines):
            if i == 0:
                if self.marine_tag1 is None:
                    self.marine_tag1 = marine.tag
            else:
                prev_tags = []
                for i in range(1, num_agents+1):
                    prev_tags.append(getattr(self, f"marine_tag{i}"))
                
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
        unit_actions, done, reward = step_update_interface.moveR(self.num_step, unit_tags, marine, xcor, ycor, blue_pos, player_net) 
        self.num_step+=1    
        return unit_actions, done, reward


## Blue Agent (Opponent)
class TerranAgent2(base_agent.BaseAgent):

    def __init__(self):
        super(TerranAgent2, self).__init__()
        self.attack_coordinates = None
        for i in range(1, num_agents+1):
            setattr(self, f"marine_tag{i}", None)
        self.tank_tag = None
        self.num_step = 0
    
    def step(self, obs):
        super(TerranAgent2, self).step(obs)
        marines = get_raw_units_by_type(obs, units.Terran.Marine)
        for i, marine in enumerate(marines):
            if i == 0:
                if self.marine_tag1 is None:
                    self.marine_tag1 = marine.tag
            else:
                prev_tags = []
                for i in range(1, num_agents+1):
                    prev_tags.append(getattr(self, f"marine_tag{i}"))
                
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
        for i in range(1, len(prev_tags)+1):
            marine_tag = getattr(self, f"marine_tag{i}")
            if marine_tag:
                marine.append([unit for unit in marines if unit.tag == marine_tag][0])
        unit_actions, pos, done, reward = step_update_interface.moveB(self.num_step, unit_tags, marine, xcor, ycor) 
        self.num_step+=1
        return unit_actions, pos, done, reward



def main(unused_argv):

    agent1 = TerranAgent1()
    agent2 = TerranAgent2()

    winner_blue_cnt = 0
    winner_red_cnt = 0

    total_time=0
    total_steps=0
    max_mem=0
    total_reward=0

    episodes = 500

    filename=sys.argv[2]
    path=sys.argv[1]
    start_index = filename.find('s') + 1
    end_index = filename.find('.pth')
    step_val=filename[start_index:end_index]

    # loading the model
    player_net = Network()
    player_net.load_state_dict(torch.load(path))
    player_net.eval()

    print("Starting" + str(episodes) +" Run experiment")
    try:
        with sc2_env.SC2Env(
            map_name = map_name,
            players=[sc2_env.Agent(sc2_env.Race.terran),
                     sc2_env.Agent(sc2_env.Race.terran)],
            agent_interface_format = features.AgentInterfaceFormat(
                feature_dimensions = features.Dimensions(screen=84, minimap=64),
                use_feature_units = True,
                use_raw_units = True,
                use_raw_actions=True,
                rgb_dimensions=None
            ),
            step_mul = 100,
            game_steps_per_episode = 0,
            # visualize=True
            visualize=False
        ) as env:
            agent1.setup(env.observation_spec(), env.action_spec())
            agent2.setup(env.observation_spec(), env.action_spec())
            with open(file1Name, 'a') as ff:
                ff.write("Step: "+ str(step_val)+" Trials --------------------------------------------------------------------------------------------" + '\n')
            for tt in range(episodes):
                start = time.time()
                tracemalloc.start()
                timesteps = env.reset()
                agent1.reset()
                agent2.reset()
                step_num = 0
                ep_reward = 0
                pos = (30, 28)
                pos = [pos] * num_agents
                while True:
                    agent1_actions, doneR, reward1 = agent1.step(timesteps[0], pos, player_net)
                    agent2_actions, pos, doneB, reward2 = agent2.step(timesteps[1])
                    step_actions = [agent1_actions, agent2_actions]
                    ep_reward += (reward1 + reward2)
                    ## If red agent reaches the blue base stop
                    if doneR:
                        winner_red_cnt += 1
                        with open(file1Name, 'a') as ff:
                            ff.write("Trial " + str(tt) + " Winner: Red" + '\t')
                        break
                    ## If blue agent reaches the red base stop
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
                    time_each_ep=time.time() - start
                    total_time+=time_each_ep
                    mem = tracemalloc.get_traced_memory()[1]/(10**6)
                    total_steps+=step_num
                    if(max_mem < mem):
                        max_mem = mem
                    tracemalloc.stop()
                    total_reward+=ep_reward
                    ff.write("Total Reward:" + str(ep_reward) + "\n")
        line = "step: "+ str(step_val)+", Win Percentage: "+ str((winner_red_cnt/episodes)*100)+", time avg: "+ str(total_time/episodes)+ " s, Maximum memory: "+str(max_mem)+" MB, Average Reward: "+str(total_reward/episodes)+ ", Steps taken: "+str(total_steps/episodes)
        with open(file2Name, 'a') as f:
            f.write(line + '\n')
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app.run(main)

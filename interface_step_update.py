#step_update
#take input as the location of the unit and output the step
from pysc2.lib import actions, features, units
from n_marine_interface import num_agents
import numpy as np
import random


## Game setup
red_base = (7,0)
blue_base = (0,7)
mountains = [(2,3), (3,3), (2,4), (3,4), (4,4), (4,5)]
directions = ['up', 'down', 'left', 'right', 'nop']
goal_dist=0
blue_done=0
## Grid size
size = 8
EPS_VAL_START = 1.0
OPPO_RANDOMNESS_START = 0.3
OPPO_RANDOMNESS_END = 0.05
blue_randomness=min(OPPO_RANDOMNESS_START, EPS_VAL_START)
max_dist = abs(blue_base[0] - red_base[0]) + abs(blue_base[1] - red_base[1])



# getting the number of marines 
def total_number_of_soldiers():
    num_of_soldiers = input("Enter number of marines: ")
    num_of_soldiers = int(num_of_soldiers)
    return num_of_soldiers

# num_agents=5
blue_pref_dir = [random.randint(0, 1) for _ in range(num_agents)]



def validMove(pos, dir):
    if dir == 'nop':
        return True
    elif dir == 'up':
        new_pos = (pos[0], pos[1]+1)
    elif dir == 'down':
        new_pos = (pos[0], pos[1]-1)
    elif dir == 'left':
        new_pos = (pos[0]-1, pos[1])
    elif dir == 'right':
        new_pos = (pos[0]+1, pos[1])
    else:
        new_pos = (pos[0], pos[1])
    if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] > size-1 or new_pos[1] > size-1:
        return False
    if new_pos in mountains:
        return False
    return True

def calculate_coords(x, y):
        x_co = (x - 30) // 10
        y_co = abs((y - 28) // 10 - 7)
        return x_co, y_co


## method for Blue agent
def moveB(num_step, unit_tags, marine, xcor, ycor):
    ## Opponent Blue agent moves with a stochastic greedy policy based on
    ## its current manhattan distance from red base
    blue_poses = []

    # calculating the coordinates of the blue marines in the grid
    for marine_obj in marine:
        x_co, y_co = calculate_coords(marine_obj.x, marine_obj.y)
        blue_poses.append((x_co, y_co))

    
    # randomly selecting the directions or move commands for the blue marines
    agent_step = []
    for idx in range(num_agents):
        if random.random() <= max(blue_randomness, OPPO_RANDOMNESS_END):
                
                ## Making it easier
                dir = random.choice(directions)
                if validMove(blue_poses[idx], dir):
                    agent_step.append(dir)
                else:
                    agent_step.append("nop")
        else:
            if blue_pref_dir[idx]:
                y_dis = blue_poses[idx][1] - red_base[1]
                if y_dis > 0:
                    agent_step.append('down')
                elif y_dis < 0:
                    agent_step.append('up')
                else:
                    x_dis = blue_poses[idx][0] - red_base[0]
                    if x_dis > 0:
                        agent_step.append('left')
                    elif x_dis < 0:
                        agent_step.append('right')
            else:
                x_dis = blue_poses[idx][0] - red_base[0]
                if x_dis > 0:
                    agent_step.append('left')
                elif x_dis < 0:
                    agent_step.append('right')
                else:
                    y_dis = blue_poses[idx][1] - red_base[1]
                    if y_dis > 0:
                        agent_step.append('down')
                    elif y_dis < 0:
                        agent_step.append('up')
            if validMove(blue_poses[idx], agent_step[idx]):
                agent_step[idx] = agent_step[idx]
            else:
                agent_step[idx] = "nop"

        unit_actions = []

        print("At step:", num_step, " BLUE agent location:", (x_co, y_co),"took action:", agent_step[idx])
        blue_pos = []
        done = False
        global blue_done
    
    # changing the coordinates of blue marines according to the direction
    for i in range(num_agents):     
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
        blue_pos.append((xcor[i],ycor[i]))

        # checking if the blue marines have reached the red base, in which case blur team wins
        x_co, y_co = calculate_coords(xcor[i], ycor[i])
        if (x_co, y_co) == red_base:
            done = True
            blue_done=1
        unit_actions.append(actions.RAW_FUNCTIONS.Move_pt("now", unit_tags[i], (xcor[i],ycor[i])))
        result = {"unit tag": [unit_tags[i]], "location": [xcor[i],ycor[i]]}
        print("B:",result)
    reward = 0
    # calculating the reward based on the red marines postions
    if done:
        reward = -250*goal_dist 
    return unit_actions, blue_pos, done, reward


## method for red agent
def moveR(num_step, unit_tags, marine, xcor, ycor, blue_pos, player_net):
    ## Move Red agent based on the learned policy by consulting the Q table 
    unit_actions = []
    agent_step=[]
    oppo_x_values=[]
    oppo_y_values=[]
    reward = [0] * num_agents
    reward_sum=0
    obs = [[] for _ in range(num_agents)]


    # getting locations of the red marines
    for i in range(num_agents):
        x_co, y_co = calculate_coords(marine[i].x, marine[i].y)
        print("At step:", num_step, " RED agent location:", (x_co, y_co))

    # getting the location of blue marines
    for i, (oppo_x, oppo_y) in enumerate(blue_pos):
        oppo_x, oppo_y = calculate_coords(oppo_x, oppo_y)
        oppo_x_values.append(oppo_x)
        oppo_y_values.append(oppo_y)

    # moving red marine based on the action from player_net considering blue marines' locations
    for i in range(num_agents):
        x_co, y_co = calculate_coords(marine[i].x, marine[i].y)
        agent_obs = [x_co, y_co]
        for j in range(num_agents):
            agent_obs.append(oppo_x_values[j])
            agent_obs.append(oppo_y_values[j])
        obs[i] = np.array(agent_obs, dtype=np.float32)
        agent_step.append([directions[player_net.act(obs[i])]])
        reward[i] = 0
        print(agent_step[i])
        if not validMove((x_co, y_co), agent_step[i]):
            agent_step[i] = ["nop"]
            reward[i] = -200
        else:
            reward[i] = -1


        print("At step:", num_step, " agent location:", (x_co, y_co),"took action:", agent_step[i])
        done = False
    global goal_dist
    total_dist=0
    
    # move the red marines based on the actions from previous snippet 
    for i in range(num_agents):     
        ycor.append(marine[i].y)
        xcor.append(marine[i].x)   
        if(agent_step[i][0]=="up"):
            ycor[i]=int(ycor[i])-10
        if(agent_step[i][0]=="down"):
            ycor[i]=int(ycor[i])+10
        if(agent_step[i][0]=="left"):
            xcor[i]=int(xcor[i])-10
        if(agent_step[i][0]=="right"):
            xcor[i]=int(xcor[i])+10
        agent_pos = (xcor[i],ycor[i])
        x_co, y_co = calculate_coords(agent_pos[0], agent_pos[1])
        red_pos=(x_co, y_co)

        # checking if the red marine has moved the blue base, in that case red wins and reward is calculated.
        if (x_co, y_co) == blue_base:
            done = True
        unit_actions.append(actions.RAW_FUNCTIONS.Move_pt("now", unit_tags[i], (xcor[i],ycor[i])))
        result = {"unit tag": [unit_tags[i]], "location": [xcor[i],ycor[i]]}
        print("R:",result)

        # distance is calculated for blue teams rewards in case blue team wins.
        dist = (abs(blue_base[0] - red_pos[0]) + abs(blue_base[1] - red_pos[1])) / max_dist
        total_dist+=dist
        
        if done:
            reward[i] = 500
    goal_dist=total_dist
    
    # summing up rewards for each marine in red team.
    for i in range(num_agents):
        reward_sum+=reward[i]
    return unit_actions, done, reward_sum

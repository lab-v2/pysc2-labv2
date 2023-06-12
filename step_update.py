#step_update
#take input as the location of the unit and output the step
from pysc2.lib import actions, features, units
import sys
import numpy as np
import random as rng
import pickle
import time

## Read Learned Policy as a Q table from pkl file
with open('pr-qtable.npy', 'rb') as fp:
    q_table = np.load(fp)

## A simple Wrapper for interfacing with PySC2 as a grid world
## the move selector methods also provide information about the rewards

directions = ['up', 'down', 'left', 'right']

## Game setup
red_base = (7,0)
blue_base = (0,7)
mountains = [(2,3), (3,3), (2,4), (3,4), (4,4), (4,5)]
## Grid size
size = 8


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

## method for Blue agent
def my_methodB(num_step, unit_tags, marine, xcor, ycor):
    ## Opponent Blue agent moves with a stochastic greedy policy based on
    ## its current manhattan distance from red base
    x_co = (marine[0].x - 30) // 10
    y_co = abs((marine[0].y - 28) // 10 - 7)

    blue_pos = (x_co, y_co)

    if rng.randint(0,9) < 3:
        dir = rng.choice(directions)
        if validMove(blue_pos, dir):
            agent_step = [dir]
        else:
            agent_step = ["nop"]
    else:
        x_dis = blue_pos[0] - red_base[0]
        if x_dis > 0:
            agent_step = ['left']
        elif x_dis < 0:
            agent_step = ['right']
        else:
            y_dis = blue_pos[1] - red_base[1]
            if y_dis > 0:
                agent_step = ['down']
            elif y_dis < 0:
                agent_step = ['up']
        if not validMove(blue_pos, agent_step[0]):
            dir = rng.choice(directions)
            if validMove(blue_pos, dir):
                agent_step = [dir]
            else:
                agent_step = ["nop"]


    unit_actions = []

    print("At step:", num_step, " BLUE agent location:", (x_co, y_co),"took action:", agent_step)
    blue_pos = None
    done = False
    for i in range(1):     
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
            blue_pos = (xcor[i],ycor[i])

            x_co = (blue_pos[0] - 30) // 10
            y_co = abs((blue_pos[1] - 28) // 10 - 7)
            if (x_co, y_co) == red_base:
                done = True
            unit_actions.append(actions.RAW_FUNCTIONS.Move_pt("now", unit_tags[i], (xcor[i],ycor[i])))
            result = {"unit tag": [unit_tags[i]], "location": [xcor[i],ycor[i]]}
            print("B:",result)
    reward = 0
    if done:
        reward = -100   
    return unit_actions, blue_pos, done, reward

## method for red agent
def my_methodR(num_step, unit_tags, marine, xcor, ycor, blue_pos):
    ## Move Red agent based on the learned policy by consulting the Q table 
    unit_actions = []

    print("At step:", num_step, " RED agent location:", (marine[0].x, marine[0].y))

    x_co = (marine[0].x - 30) // 10
    y_co = abs((marine[0].y - 28) // 10 - 7)

    oppo_x = (blue_pos[0] - 30) // 10
    oppo_y = abs((blue_pos[1] - 28) // 10 - 7)

    print("And Opponent location: ",(oppo_x, oppo_y))
    print("Q values")
    print(q_table[x_co][y_co][oppo_x][oppo_y])
    
    ## Agents current location and opponents locations are used as state information
    ## to access the action Q values to select the best performing action
    agent_step = [directions[np.argmax(q_table[x_co][y_co][oppo_x][oppo_y])]]
    reward = 0
    if not validMove((x_co, y_co), agent_step[0]):
        agent_step = ["nop"]
        reward = -10
    else:
        reward = -1


    print("At step:", num_step, " agent location:", (x_co, y_co),"took action:", agent_step)
    # time.sleep(1)
    done = False
    for i in range(1):     
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
            agent_pos = (xcor[i],ycor[i])

            x_co = (agent_pos[0] - 30) // 10
            y_co = abs((agent_pos[1] - 28) // 10 - 7)
            if (x_co, y_co) == blue_base:
                done = True
            unit_actions.append(actions.RAW_FUNCTIONS.Move_pt("now", unit_tags[i], (xcor[i],ycor[i])))
            result = {"unit tag": [unit_tags[i]], "location": [xcor[i],ycor[i]]}
            print("R:",result)
    if done:
        reward = 100
    return unit_actions, done, reward

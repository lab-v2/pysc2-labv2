#step_update
#take input as the location of the unit and output the step
from pysc2.lib import actions, features, units
import sys
def my_methodB(num_step, unit_tags, marine, xcor, ycor, length):
    B=[]
    # print("score: ",score)
    user_input = input("Please enter a list of directions for team Blue: ")
    if user_input == "end":
        sys.exit()

    directions_list = eval(user_input)  # Using eval to convert the string input to a list

    if isinstance(directions_list, list):  # Check that the user input is a list
        B.append(directions_list)
    unit_actions = []
    # do something with list1 and list2
    # if(len(B) <= num_step):
    #         return actions.RAW_FUNCTIONS.no_op()
    
    agent_step = B[len(B)-1]
    for i in range(length):     
            ycor.append(marine[i].y)
            xcor.append(marine[i].x)   
            if(agent_step[i]=="up"):
                ycor[i]=int(ycor[i])-10
            if(agent_step[i]=="down"):
                ycor[i]=int(ycor[i])+10
            if(agent_step[i]=="left"):
                xcor[i]=int(xcor[i])+10
            if(agent_step[i]=="right"):
                xcor[i]=int(xcor[i])-10
            unit_actions.append(actions.RAW_FUNCTIONS.Attack_pt("now", unit_tags[i], (xcor[i],ycor[i])))
            result = {"unit tag": [unit_tags[i]], "location": [xcor[i],ycor[i]]}
            print("B:",result)            
    return unit_actions


def my_methodR(num_step, unit_tags, marine, xcor, ycor, length):
    R=[]
    # print("score: ",score)
    user_input = input("Please enter a list of directions for team Red: ")
    if user_input == "end":
        sys.exit()
    
    directions_list = eval(user_input)  # Using eval to convert the string input to a list

    if isinstance(directions_list, list):  # Check that the user input is a list
        R.append(directions_list)
    unit_actions = []
    # do something with list1 and list2
    # if(len(R) <= num_step):
    #         return actions.RAW_FUNCTIONS.no_op()
    
    agent_step = R[len(R)-1]
    for i in range(length):     
            ycor.append(marine[i].y)
            xcor.append(marine[i].x)   
            if(agent_step[i]=="up"):
                ycor[i]=int(ycor[i])-10
            if(agent_step[i]=="down"):
                ycor[i]=int(ycor[i])+10
            if(agent_step[i]=="left"):
                xcor[i]=int(xcor[i])+10
            if(agent_step[i]=="right"):
                xcor[i]=int(xcor[i])-10
            unit_actions.append(actions.RAW_FUNCTIONS.Attack_pt("now", unit_tags[i], (xcor[i],ycor[i])))
            result = {"unit tag": [unit_tags[i]], "location": [xcor[i],ycor[i]]}
            print("R:",result)       
    return unit_actions
    #return result
    # [[up,nop,up],[up,nop,up]] [[right,down,right],[right,down,right]] 
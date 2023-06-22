#step_update
#take input as the location of the unit and output the step
from pysc2.lib import actions, features, units
import sys
def total_number_of_soldiers():
    num_of_soldiers = input("Enter a number: ")
    num_of_soldiers = int(num_of_soldiers)
    return num_of_soldiers

def moveUnits(agent_step, marine, xcor, ycor, unit_tags, length):
    unit_actions = []
    for i in range(length):
        ycor.append(marine[i].y)
        xcor.append(marine[i].x)
        if agent_step[i] == "up":
            ycor[i] = int(ycor[i]) - 10
        if agent_step[i] == "down":
            ycor[i] = int(ycor[i]) + 10
        if agent_step[i] == "left":
            xcor[i] = int(xcor[i]) + 10
        if agent_step[i] == "right":
            xcor[i] = int(xcor[i]) - 10
        unit_actions.append(actions.RAW_FUNCTIONS.Attack_pt("now", unit_tags[i], (xcor[i], ycor[i])))
        result = {"unit tag": [unit_tags[i]], "location": [xcor[i], ycor[i]]}
        print(result)
    return unit_actions


def getUserInput(team_name):
    user_input = input(f"Please enter a list of directions for team {team_name}: ")
    if user_input == "end":
        sys.exit()
    directions_list = eval(user_input)  # Using eval to convert the string input to a list
    if isinstance(directions_list, list):  # Check that the user input is a list
        return directions_list
    else:
        return None


def blueSteps(num_step, unit_tags, marine, xcor, ycor, length):
    B = []
    directions_list = getUserInput("Blue")
    if directions_list is None:
        print("Invalid input")
        return []
    B.append(directions_list)
    agent_step = B[-1]
    unit_actions = moveUnits(agent_step, marine, xcor, ycor, unit_tags, length)
    return unit_actions


def redSteps(num_step, unit_tags, marine, xcor, ycor, length):
    R = []
    directions_list = getUserInput("Red")
    if directions_list is None:
        print("Invalid input")
        return []
    R.append(directions_list)
    agent_step = R[-1]
    unit_actions = moveUnits(agent_step, marine, xcor, ycor, unit_tags, length)
    return unit_actions

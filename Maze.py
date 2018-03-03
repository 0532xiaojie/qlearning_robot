"""
Template for implementing Maze
"""

import numpy as np
import random as rand

class Maze(object):
    def __init__(self,
            data,
            reward_walk = -1,
            reward_obstacle = -1,
            reward_quicksand = -100,
            reward_goal = 1,
            random_walk_rate = 0.2,
            verbose = False):

        #TODO
        self.data = data
        self.reward_walk = reward_walk
        self.reward_obstacle = reward_obstacle
        self.reward_quicksand = reward_quicksand
        self.reward_goal = reward_goal
        self.random_walk_rate = random_walk_rate
        self.verbose = verbose

    #return the start position of the robot
    def get_start_pos(self):
        for i in range(len(self.data)):
            if '2' in self.data[i]:
                return (i,self.data[i].index('2'))

    #return the goal position of the robot
    def get_goal_pos(self):
        for i in range(len(self.data)):
            if '3' in self.data[i]:
                return (i,self.data[i].index('3'))

    # move the robot and report new position and reward
    # Note that robot cannot step into obstacles nor step out of the map
    # Note that robot may ignore the given action and choose a random action
    # 0:up 1:left 2:down 3:right
    def move(self, oldpos, a):
        choi = [a,-1]
        mov = rand.choices(choi,[(1-self.random_walk_rate),self.random_walk_rate])
        if mov[0]==a:
            act=a
        else:
            act=rand.randint(0,3)
        #newpos = oldpos
        resu = {
            0: lambda sp: sp if sp[0]==0 or self.data[sp[0]-1][sp[1]]=='1' else (sp[0]-1,sp[1]),
            1: lambda sp: sp if sp[1]==0 or self.data[sp[0]][sp[1]-1]=='1' else (sp[0],sp[1]-1),
            2: lambda sp: sp if sp[0]==9 or self.data[sp[0]+1][sp[1]]=='1' else (sp[0]+1,sp[1]),
            3: lambda sp: sp if sp[1]==9 or self.data[sp[0]][sp[1]+1]=='1' else (sp[0],sp[1]+1)
            }        
        #newpos = (oldpos[0], oldpos[1])
        newpos = resu[act](oldpos)
        if self.data[newpos[0]][newpos[1]]=='3':
            reward = self.reward_goal
        elif self.data[newpos[0]][newpos[1]]=='5':
            reward = self.reward_quicksand
        elif newpos == oldpos:
            reward = self.reward_obstacle
        else:
            reward = self.reward_walk

        # return the new, legal location and reward
        return newpos, reward

    # print out the map
    def print_map(self):
        data = self.data
        print("--------------------")
        for row in range(0, data.shape[0]):
            for col in range(0, data.shape[1]):
                if data[row,col] == 0: # Empty space
                    print(" ",end="")
                if data[row,col] == 1: # Obstacle
                    print("X",end="")
                if data[row,col] == 2: # Start
                    print("S",end="")
                if data[row,col] == 3: # Goal
                    print("G",end="")
                if data[row,col] == 5: # Quick sand
                    print("~",end="")
            print()
        print("--------------------")

    # print the map and the trail of robot
    def print_trail(self, trail):
        data = self.data
        trail = data.copy()
        for pos in trail:

            #check if position is valid
            if not (    0 <= pos[0] < data.shape[0]
                    and 0 <= pos[1] < data.shape[1]):
                print("Warning: Invalid position in trail, out of the world")
                return

            if data[pos] == 1:  # Obstacle
                print("Warning: Invalid position in trail, step on obstacle")
                return

            #mark the trail
            if data[pos] == 0:  # mark enter empty space
                trail[pos] = "."
            if data[pos] == 5:  # make enter quicksand
                trail[pos] = "@"

        print("--------------------")
        for row in range(0, trail.shape[0]):
            for col in range(0, trail.shape[1]):
                if trail[row, col] == 0:  # Empty space
                    trail[row, col] = " "
                if trail[row, col] == 1:  # Obstacle
                    trail[row, col] = "X"
                if trail[row, col] == 2:  # Start
                    trail[row, col] = "S"
                if trail[row, col] == 3:  # Goal
                    trail[row, col] = "G"
                if trail[row, col] == 5:  # Quick sand
                    trail[row, col] = "~"

                print(trail[row, col], end="")
            print()
        print("--------------------")

"""
Train a Q Learner in a navigation problem.
"""

import numpy as np
import random as rand
import QLearner as ql
import Maze
import csv


# convert the position to a single integer state
def to_state(pos):
    return pos[0]*10+pos[1]


# train learner to go through maze multiple epochs
# each epoch involves one trip from start to the goal or timeout before reaching the goal
# return list of rewards of each trip
def train(maze, learner, epochs=500, timeout = 100000, verbose = False):
    rewards = np.zeros(epochs)
    start = maze.get_start_pos()
    goal = maze.get_goal_pos()
    action = learner.querysetstate(to_state(start))
    itertry=0
    while itertry<epochs:
        timecnt=0
        i_reward=0
        robopos = start
        while robopos != goal and timecnt != timeout:
            newpos, reward = maze.move(robopos, action)
            robopos = newpos
            action = learner.query(to_state(robopos), reward)
            i_reward += reward
            if reward==-100:
                break
            timecnt +=1
        rewards[itertry]=i_reward
        if verbose: print('iteration ',itertry, ' reward: ',i_reward)
        itertry+=1
    if verbose: print(rewards)
    return rewards


# run the code to train a learner on a maze
def maze_qlearning(filename):

    #initialize maze object
    with open(filename, 'r') as fin:
        cin = csv.reader(fin)
        mazerows = [row for row in cin] 
    mazz=Maze.Maze(data=mazerows, verbose = False)
    #initialize learner object
    learner = ql.QLearner(num_states = 100, num_actions = 4, alpha = 0.2, gamma = 0.9, rar = 0.5,
                          radr = 0.99, verbose = False)
    #execute train(maze, learner)
    all_rewards = train(mazz, learner, epochs=1500)
    #return median of all rewards
    return np.median(all_rewards)

if __name__=="__main__":
    rand.seed(5)
    maze_qlearning('testworlds/world01.csv')

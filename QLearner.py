"""
Template for implementing QLearner  
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self,
        num_states=100,
        num_actions = 4,
        alpha = 0.2,
        gamma = 0.9,
        rar = 0.5,
        radr = 0.99,
        verbose = False):

        #TODO
        self.verbose = verbose
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.verbose = verbose
        self.s = 0
        self.a = 0
        self.Q = np.random.uniform(-1, 1, size=(num_states, num_actions))
        #self.Q = np.zeros((num_states, num_actions))


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """

        self.s = s
        actrand=np.random.random()
        if actrand<self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.Q[s, :])
        
        self.a = action
        
        if self.verbose: print("s =", s,"a =",action)
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        #Update the Q table Q[s, a] <- (1-alpha)Q[s, a]+alpha* (r + gamma*max_a'*Q[s', a'])
        self.Q[self.s, self.a] = (1 - self.alpha)*self.Q[self.s, self.a] + \
            self.alpha*(r+self.gamma*np.max(self.Q[s_prime,:]))
        self.s = s_prime
        self.a = self.querysetstate(self.s)
        self.rar *= self.radr
        
        if self.verbose: print("s =", s_prime,"a =",self.a,"r =",r)
        return self.a


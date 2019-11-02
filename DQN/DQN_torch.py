import random
import gym
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from collections import deque


class DQN_model(nn.Module):
    def __init__(self,num_actions):
        self.conv1=nn.Conv2d(3,32,8,stride=4)
        self.conv2=nn.Conv2d(32,64,4,stride=2)
        self.conv3=nn.Conv2d(64,64,3,stride=1)
        self.fcc1=nn.Linear(85,512)
        self.fcc2=nn.Linear(512,num_actions)

    def forward(self,x):
        x=F.relu(self.conv1(x))
        x=F.relu(self.conv2(x))
        x=F.relu(self.conv3(x))
        x=x.view(x.size(0),-1)
        x=F.relu(self.fcc1(x))
        x=self.fcc2(x)

        return x
        
class DQN_Agent:

    def __init__(self,num_states,num_actions):
        self.num_states=num_states
        self.num_actions=num_actions
        #DEBUG make a memory here
        self.discount=0.9
        self.epsilon=1
        self.min_epsilon=0.1
        self.epsilon_decay_rate=0.995
        self.update_rate=1000

        self.base_model=DQN_model()
        self.target_model=DQN_model()
        self.target_model.load_state_dict(self.base_model.state_dict())
        self.memory=deque(maxlen=4500)

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

    def act(self,state):

        if np.random.rand() <= self.epsilon:
            return random.choice(range(self.num_actions))
        
        act_probs=self.base_model(state)

        return np.argmax(act_probs.squeeze())

    def replay(self,bs):

        minibatch=random.sample(self.memory,bs)

        for memory_element in self.memory:
            state=memory_element[0]
            action=memory_element[1]
            reward=memory_element[2]
            next_state=memory_element[3]
            done=memory_element[4]

        assert(done==(reward==0))
        if reward==0:
            target=reward
        else:
            target=(reward+self.discount*np.max(self.target_model(next_state)))
        
        current_target=self.base_model(state)
        






        
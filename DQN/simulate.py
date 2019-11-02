import gym
from DQN_torch import DQN_Agent, DQN_model
from util import *
from collections import deque

env = gym.make('MsPacman-v0')
num_states = (88, 80, 1)
num_actions = env.action_space.n

pacmanAgent = DQN_Agent(num_states, num_actions)

# Parameters

num_epochs = 500
bs = 1
avg_reward = 0
fps_factor = 4
wait_time = 90
T = 0

done = False


# Train loop
for i in range(num_epochs):
    print("epoch: " + str(i))
    total_reward = 0
    score = 0
    state = preprocess(env.reset())
    print("Called preprocess")
    frame_queue = deque(maxlen=fps_factor)
    frame_queue.append(state)

    for t in range(wait_time):
        env.step(0)

    print("Waiting done")

    for t in range(2):
        env.render()
        T += 1

    if T % pacmanAgent.update_rate == 0:
        pacmanAgent.update_target_from_base()

    print("Updating target model done")

    state = mergeFrames(frame_queue, fps_factor)

    action = pacmanAgent.act(state)
    nextState, reward, done, _ = env.step(action)
    print("Action found")

    nextState = preprocess(nextState)
    frame_queue.append(nextState)
    nextState = mergeFrames(frame_queue, fps_factor)

    pacmanAgent.remember(state, action, reward, nextState, done)

    print("remember called")

    state = nextState
    score = score + reward
    reward = reward - 1
    total_reward += reward

    if done:
        avg_reward = avg_reward + score

        print("epoch: " + str(i))
        print("game_score: " + str(score))
        print("reward: " + str(total_reward))

        break

    if len(pacmanAgent.memory) > bs:
        pacmanAgent.replay(bs)


pacmanAgent.save_model("models/dqn_pacman.pth")

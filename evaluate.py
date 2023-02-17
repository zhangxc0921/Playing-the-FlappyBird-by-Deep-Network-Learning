from tqdm import tqdm

import rl_utils
from FlayppyBird import Qnet
import torch
import flappy_bird_gym
import matplotlib.pyplot as plt

class runFlappyBird:
    def __init__(self, path, device):
        self.device = device
        try:
            self.q_net = torch.load(path)
        except:
            print("模型路径错误，请重新检查")
            exit(0)

    def take_action(self, state):
        state = torch.tensor([state], dtype=torch.float).to(self.device)
        action = self.q_net(state).argmax().item()
        return action

def evaluate(agent,evaluate_episode):
    rewards=0
    with tqdm(range(evaluate_episode), desc="model_evaluate: %d" % i,colour='blue') as tbar:
        for j in range(evaluate_episode):
            state = env.reset()
            env.render()
            while True:
                action = agent.take_action(state)
                next_state, reward, done, _ = env.step(action)
                env.render()
                state = next_state
                rewards += reward
                if done:
                    break
            rewards += 100000
            tbar.update(1)
            tbar.set_postfix({'mean_reward': rewards / (j + 1)})
    return rewards/(evaluate_episode)

######### 参数 ##########
index = 27
epoch_list = list(range(1, index + 1))
rewards_list = []
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
evaluate_episode = 10
######### 参数 ##########

if __name__ == '__main__':
    env = flappy_bird_gym.make('FlappyBird-v0')
    env.seed(0)
    # for i in range(index):
    for i in [6]:
        path = f"./model4/2023-02-17_q_net_{i}.pth"
        agent = runFlappyBird(path, device)
        rewards =evaluate(agent,evaluate_episode)
        rewards_list.append(rewards)
    env.close()
    rewards_list = rl_utils.moving_average(rewards_list, 9)
    plt.plot(epoch_list, rewards_list)
    plt.xlabel('Episodes')
    plt.ylabel('Returns')
    plt.title('DQN on Flappy Bird')
    plt.show()
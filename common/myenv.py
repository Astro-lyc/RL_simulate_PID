import sys
import os

curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径
import numpy as np
import torch

from common.helicopter_nonlinear_function import *


class Space:
    def __init__(self, shape):
        self.shape = (shape,)


class MyEnv:
    def __init__(self, ):
        self.reset()

    # 重置环境
    def reset(self):
        self.observation_space = Space(6)
        self.action_space = Space(2)
        self.reward = 0
        self.reward_rate = 10  # todo 奖励10倍于距离缩小
        # fixme 设定一个最终状态（悬停目标）
        self.final_state = np.array([25 / 180 * math.pi, 0, 0, 0, 0, 0])  # 最终需要的观测值
        self.last_observation = np.zeros((len(self.final_state)))  # 最近一次的观测 -> 初始值是0，可修改
        self.last_distance = self.o_distance(self.final_state, self.last_observation)  # 初始化距离比较量
        self.total_step = 1
        self.pid_list = []
        return self.last_observation

    # 欧式距离
    def o_distance(self, vector1, vector2):
        return np.sqrt(np.sum(np.square(vector1 - vector2)))

    def seed(self, seed):
        np.random.seed(seed)

    # 回合是否或者
    def is_dead(self, state: np.array):
        # d
        e = state[0] > 70 / 180 * math.pi or state[0] < -15 / 180 * math.pi
        if e:
            print('e超出')
        pitch = state[1] > 30 / 180 * math.pi or state[1] < -30 / 180 * math.pi
        if pitch:
            print('pitch超出')
        travel = state[2] > 30 / 180 * math.pi or state[2] < -30 / 180 * math.pi
        if travel:
            print('travel超出')
        # v
        e_v4 = state[3] > 0.50 or state[3] < -0.50
        if e_v4:
            print('e_v4超出')
        p_v5 = state[4] > 0.40 or state[4] < -0.40
        t_v6 = state[5] > 0.40 or state[5] < -0.40
        return e or pitch or travel or e_v4 or p_v5 or t_v6

    # 定义奖励：目前状态距目标的距离与前一次状态距目标的距离的差值按比例缩放
    def get_reward(self, state: np.ndarray):
        return -self.o_distance(state[:], self.final_state[:]) * self.reward_rate

    def step(self, action: torch.Tensor):
        self.last_observation = device_next_state(self.last_observation, action.tolist())
        reward = self.get_reward(self.last_observation)
        done = (self.is_dead(self.last_observation)) or (self.total_step >= 80000)
        if done:
            print('dead')
        self.total_step += 1
        return self.last_observation, reward, done, 0

    def close(self):
        return


if __name__ == '__main__':
    env = MyEnv()
    print(env.last_distance)

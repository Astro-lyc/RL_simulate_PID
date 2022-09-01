import math
import sys
import os

curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径
import numpy as np
import torch

from quanser.hardware import HIL, MAX_STRING_LENGTH, EncoderQuadratureMode
from quanser.q_misc import Calculus

from array import array

import time


class Space():
    def __init__(self, shape):
        self.shape = (shape,)


class MyEnv():
    def __init__(self, ):
        #
        self.init_cart()
        # Set up a differentiator to get encoderSpeed from encoderCounts
        self.diff_travel = Calculus().differentiator_variable(0.1)
        self.diff_pitch = Calculus().differentiator_variable(0.1)
        self.diff_elevation = Calculus().differentiator_variable(0.1)
        next(self.diff_travel)
        next(self.diff_pitch)
        next(self.diff_elevation)
        #
        self.timestep = 0.1
        #
        self.reset()

    def init_cart(self):
        self.card = HIL()
        self.card.open("ni_pcie_6351", "0")
        self.card.set_card_specific_options("terminal_board=mx_series;", MAX_STRING_LENGTH)
        channels = array('I', [0, 1, 2])
        num_channels = len(channels)
        modes = array('i', [EncoderQuadratureMode.X4, EncoderQuadratureMode.X4, EncoderQuadratureMode.X4])
        self.card.set_encoder_quadrature_mode(channels, num_channels, modes)

    # new
    def change_v(self, *args):
        v1 = args[0]
        v2 = args[1]
        _ao_channels = array('I', [0])  #
        _ao_channels2 = array('I', [1])
        _ao_buffer = array('d', [v1])  # Voltage 1
        self.card.write_analog(_ao_channels, len(_ao_channels), _ao_buffer)
        _ao_buffer2 = array('d', [v2])  # Voltage 2
        self.card.write_analog(_ao_channels2, len(_ao_channels2), _ao_buffer2)

    # new
    def make_observa(self):
        channels = array('I', [0, 1, 2])
        num_channels = len(channels)
        buffer = array('i', [0] * num_channels)
        self.card.read_encoder(channels, num_channels, buffer)
        travel = float(buffer[0]) / 8192 * 360 / 180 * math.pi
        pitch = float(buffer[1]) / 4096 * 360 / 180 * math.pi
        elevation = float(-buffer[2]) / 4096 * 360 / 180 * math.pi

        # Differentiate encoder counts and then estimate linear speed in m/s
        delta_travel = self.diff_travel.send((buffer[0], self.timestep))
        delta_pitch = self.diff_pitch.send((buffer[1], self.timestep))
        delta_elevation = self.diff_elevation.send((-buffer[2], self.timestep))
        w_travel = delta_travel / 8192 * 360 / 180 * math.pi  # Travel Speed
        w_pitch = delta_pitch / 4096 * 360 / 180 * math.pi  # Pitch Speed
        w_elevation = delta_elevation / 4096 * 360 / 180 * math.pi  # Elevation Speed
        # state = [travel, pitch, elevation, w_travel, w_pitch, w_elevation]
        state = [elevation, pitch, travel, w_elevation, w_pitch, w_travel]
        return np.array(state)

    # 重置环境
    def reset(self):
        self.observation_space = Space(6)
        self.action_space = Space(2)
        self.reward = 0
        self.reward_rate = 10  # todo 奖励10倍于距离缩小
        # fixme 设定一个最终状态（悬停目标）
        self.final_state = np.array([15 / 180 * math.pi, 0, 0, 0, 0, 0])  # 最终需要的观测值
        self.change_v(0.0, 0.0)
        print('sleep2')
        time.sleep(4)
        self.card.close()
        self.init_cart()
        # self.last_observation = np.zeros((len(self.final_state)))  # 最近一次的观测 -> 初始值是0，可修改
        self.last_observation = self.make_observa()  # 最近一次的观测 -> 初始值是0，可修改
        self.last_distance = self.o_distance(self.final_state[:], self.last_observation[:])  # 初始化距离比较量
        self.total_step = 1
        return self.last_observation

    # 欧式距离
    def o_distance(self, vector1, vector2):
        return np.sqrt(np.sum(np.square(vector1 - vector2)))

    def seed(self, seed):
        np.random.seed(seed)

    # def sample(self):
    #     a = np.random.uniform(low=-1, high=1, size=(1, 3))[0]
    #     return a * self.action_bound / 5

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
        # TODO 每个回合的步骤是否超过阈值，判断是否结束
        # self.last_observation = device_next_state(self.last_observation, action.tolist())
        ac_real_v_list = (action * 1).tolist()
        self.change_v(*ac_real_v_list)
        self.last_observation = self.make_observa()
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

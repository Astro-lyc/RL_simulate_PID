import numpy as np
import matplotlib.pyplot as plt


def sat_function(x):
    return 200 * np.tanh(x / 100)


def randfloat(num, l, h):
    if l > h:
        return None
    else:
        a = h - l
        b = h - a
        out = (np.random.rand(num) * a + b).tolist()
        out = np.array(out)
        return out


def psi_bound(psi):
    if np.pi <= psi <= np.pi * 2:
        return psi - np.pi * 2
    elif -np.pi >= psi >= -2 * np.pi:
        return psi + np.pi * 2
    else:
        return psi


class Cat():
    def __init__(self, time_step, state_bound, action_bound, break_reward=1e-6,
                 eta=np.array([0, 0, np.arctan((4 / 7) * np.cos(0 / 7))]),
                 nv=np.array([1e-5, 1e-5, 1e-5])):
        self.step_seq = time_step  # 时间序列
        self.step_size = time_step[1] - time_step[0]  # 步长
        self.max_step = len(time_step)  # 总长度
        self.step_time = 0  # 当前时间
        self.reward = 0
        self.want_dis = 1.5

        self.break_reward = break_reward

        self.action_bound = action_bound  # 动作值域
        self.x_bound = state_bound[0]  # x值域
        self.y_bound = state_bound[1]  # y值域
        self.tau_bound = state_bound[2]  # tau值域

        self.eta_init = eta  # 初始eta
        self.nv_init = nv  # 初始nv
        self.eta = eta
        self.nv = nv
        self.state = np.append(self.eta, self.nv)
        self.observation = np.array([self.eta[0], self.eta[1], self.eta[2],
                                     self.x_desire(self.step_seq[self.step_time + 1]),
                                     self.y_desire(self.step_seq[self.step_time + 1]),
                                     self.tau_desire(self.step_seq[self.step_time + 1])])

        self.action_space = np.array([0, 0, 0])
        self.x_error = 0
        self.x_error_last = 0
        self.y_error = 0
        self.y_error_last = 0
        self.tau_error = 0

        self.x_trajectory = []
        self.y_trajectory = []
        self.tau_trajectory = []
        self.desire_x_trajectory = []
        self.desire_y_trajectory = []
        self.desire_tau_trajectory = []
        self.reward_trajectory = []
        self.action_trajectory_1 = []
        self.action_trajectory_2 = []
        self.action_trajectory_3 = []

        self.draw_flag = False
        self.draw_time = 0

        self.pic_index = 0

    def oen_dim_T(self, a):  # 转置
        return a.reshape(a.shape[0], 1)

    def x_desire(self, t):
        return t

    def y_desire(self, t):
        return 4 * np.sin(t / 7)
        # return 0*t
        # return 1e-6

    def tau_desire(self, t):
        return np.arctan((4 / 7) * np.cos(t / 7))
        # return 0*t
        # return 1e-6

    def in_bound(self, x, bound):
        if x >= bound:
            return bound
        elif x <= -bound:
            return -bound
        else:
            return x

    def mdlDerivatives(self, x, u, t=0):
        Tau = self.oen_dim_T(u)

        x_eta = x[0]
        y_eta = x[1]
        psi_eta = x[2]
        u_nv = x[3]
        v_nv = x[4]
        r_nv = x[5]

        eta = np.array([x_eta, y_eta, psi_eta])
        eta = self.oen_dim_T(eta)
        nv = np.array([u_nv, v_nv, r_nv])
        nv = self.oen_dim_T(nv)
        M_eta = np.array([[25.8, 0, 0],
                          [0, 24.6612, 1.0948],
                          [0, 0.0948, 2.76]])
        INV_Meta = np.linalg.inv(M_eta)
        C_nv = np.array([[0, 0, - 24.6612 * v_nv - 1.0948 * r_nv],
                         [0, 0, 25.8 * u_nv],
                         [-24.6612 * v_nv - 1.0948 * r_nv, - 25.8 * u_nv, 0]])
        d_11 = 0.7225 + 1.3274 * np.abs(u_nv) + 5.8864 * v_nv ** 2
        d_22 = 0.8612 + 36.2823 * np.abs(v_nv) + 8.05 * np.abs(r_nv)
        d_23 = -0.1079 + 0.845 * np.abs(v_nv) + 3.45 * np.abs(r_nv)
        d_32 = -0.1052 - 5.0437 * np.abs(v_nv) - 0.13 * np.abs(r_nv)
        d_33 = 1.9 - 0.08 * np.abs(v_nv) + 0.75 * np.abs(r_nv)

        D_nv = np.array([[d_11, 0, 0],
                         [0, d_22, d_23],
                         [0, d_32, d_33]])

        G_eta = np.array([0, 0, 0])
        G_eta = self.oen_dim_T(G_eta)
        Delta_dis = np.array([0, 0, 0])
        Delta_dis = self.oen_dim_T(Delta_dis)
        R_psi = np.array([[np.cos(psi_eta), -np.sin(psi_eta), 0],
                          [np.sin(psi_eta), np.cos(psi_eta), 0],
                          [0, 0, 1]])
        d_eta = R_psi @ nv
        d_nv = - INV_Meta @ C_nv @ nv - INV_Meta @ D_nv @ nv - INV_Meta @ G_eta - INV_Meta @ Delta_dis + Tau
        d_eta = d_eta.reshape(1, d_eta.shape[0])[0]
        d_nv = d_nv.reshape(1, d_nv.shape[0])[0]
        sys = np.append(d_eta, d_nv)
        return sys

    def runge_kutta(self, x_eta, u_nv, u):

        y = np.append(x_eta, u_nv)
        h = self.step_size
        k1 = self.mdlDerivatives(y, u)
        k2 = self.mdlDerivatives(y + h / 2 * k1, u)
        k3 = self.mdlDerivatives(y + h / 2 * k2, u)
        k4 = self.mdlDerivatives(y + h * k3, u)
        y_next = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        y_next[2] = psi_bound(y_next[2])

        if y_next[0] <= -self.x_bound or y_next[0] >= self.x_bound:
            print('position_out')
            position_flag = 0
            y_next[0] = (y_next[0] / abs(y_next[0])) * self.x_bound
        elif y_next[1] <= -self.y_bound or y_next[1] >= self.y_bound:
            print('position_out')
            position_flag = 0
            y_next[1] = (y_next[1] / abs(y_next[1])) * self.y_bound
        else:
            position_flag = 1

        return y_next, position_flag

    def get_reward(self, t, y):

        self.x_error_last = self.x_error
        self.y_error_last = self.y_error

        self.x_error = y[0] - self.x_desire(self.step_seq[t])
        self.y_error = y[1] - self.y_desire(self.step_seq[t])
        self.tau_error = y[2] - self.tau_desire(self.step_seq[t])

        if (self.x_error ** 2 + self.y_error ** 2) ** 0.5 <= self.want_dis and abs(self.tau_error) < 0.2:
            self.reward = 0

        if -(self.x_error ** 2 + self.y_error ** 2) ** 0.5 <= self.break_reward / 10:
            print('error_break: ', self.step_time, end='|')
            reward_flag = 0
        elif abs(self.tau_error) >= 2 * np.pi:
            print('tau_break:', self.step_time, end='|')
            reward_flag = 0
        else:
            reward_flag = 1
        reward = -0.5 * abs(self.x_error) - 0.5 * abs(self.y_error) - 0.1 * abs(
            self.tau_error) + 2 * self.step_time / 1000
        return reward, reward_flag

    def step(self, action):
        self.state, position_flag = self.runge_kutta(self.eta, self.nv, action)
        self.eta = self.state[:3]
        self.nv = self.state[3:]
        self.step_time += 1
        self.reward, reward_flag = self.get_reward(self.step_time, self.state)

        if reward_flag == 0:
            self.reward = self.break_reward

        if self.draw_flag:
            self.x_trajectory.append(self.eta[0])
            self.y_trajectory.append(self.eta[1])
            self.tau_trajectory.append(self.eta[2])
            self.reward_trajectory.append(self.reward)
            self.desire_x_trajectory.append(self.x_desire(self.step_seq[self.step_time]))
            self.desire_y_trajectory.append(self.y_desire(self.step_seq[self.step_time]))
            self.desire_tau_trajectory.append(self.tau_desire(self.step_seq[self.step_time]))
            self.action_trajectory_1.append(action[0])
            self.action_trajectory_2.append(action[1])
            self.action_trajectory_3.append(action[2])

        if self.step_time >= self.max_step - 1:  # 判断是否结束
            self.observation = np.array([self.eta[0], self.eta[1], self.eta[2],
                                         self.x_desire(self.step_seq[self.step_time]+self.step_size),
                                         self.y_desire(self.step_seq[self.step_time]+self.step_size),
                                         self.tau_desire(self.step_seq[self.step_time]+self.step_size)])
            return self.observation, self.reward, 1, 1
        else:
            self.observation = np.array([self.eta[0], self.eta[1], self.eta[2],
                                         self.x_desire(self.step_seq[self.step_time + 1]),
                                         self.y_desire(self.step_seq[self.step_time + 1]),
                                         self.tau_desire(self.step_seq[self.step_time + 1])])

            if self.reward <= self.break_reward:
                return self.observation, self.reward, 1, 1
            else:
                return self.observation, self.reward, 0, 1

    def reset(self):  # 重置环境
        self.step_time = 0
        self.eta = self.eta_init
        self.nv = self.nv_init
        self.state = np.append(self.eta, self.nv)

        self.observation = np.array([self.eta[0], self.eta[1], self.eta[2],
                                     self.x_desire(self.step_seq[self.step_time + 1]),
                                     self.y_desire(self.step_seq[self.step_time + 1]),
                                     self.tau_desire(self.step_seq[self.step_time + 1])])

        return self.observation

    def render(self):
        return None

    def seed(self, seed):
        np.random.seed(seed)

    def sample(self):
        a = np.random.uniform(low=-1, high=1, size=(1, 3))[0]
        return a * self.action_bound / 5


if __name__ == '__main__':
    t = np.linspace(0, 20, 1000)
    u = np.ones((t.shape[0], 3)) * np.array([0, -1,0])
    A_BOUND = np.array([200, 10, 10])
    S_BOUND = [200, 500, 500]
    boat = Boat(t, action_bound=A_BOUND, state_bound=S_BOUND)
    print(boat.sample())

    eta_init = [-15/180*3.14, 0, 0]
    nv_init = [0, 0, 0]
    eta = eta_init
    nv = nv_init
    x = []
    y = []
    tau = []
    for i in range(len(t)):
        x.append(eta[0])
        y.append(eta[1])
        tau.append(eta[2])
        y_next = boat.runge_kutta(eta, nv, u[i])
        eta = y_next[0:3]
        eta =eta[0].tolist()
        nv = y_next[3:]
        print(nv,eta)

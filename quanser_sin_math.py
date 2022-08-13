import math

from matplotlib import pyplot as plt

from common.rotor_state_calculator import nonlinearheli
# from common.myenv import MyEnv
from common.myenv_pid import MyEnv
import torch

if __name__ == '__main__':
    env = MyEnv()
    # Read Encoders channel 0,1,2
    setpoint, y, x, z, p = [], [], [], [], []

    for i in range(400):
        # v = sin(2 pi f t) ; t = i * dt(step)  f = 1Hz
        f = 1
        step = 0.1
        t = i * step
        v = math.sin(2 * math.pi * f * t) * 3
        v = 2
        p += [v]

        v = torch.tensor([v, v])
        s_, r, done, _ = env.step(v)
        print(s_)
        #
        y += [s_[0]]
    plt.plot(y, label='e')
    plt.plot(p, label='v')
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.legend()
    plt.show()

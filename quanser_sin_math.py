import math

from matplotlib import pyplot as plt

from common.rotor_state_calculator import nonlinearheli
# from common.myenv import MyEnv
from common.myenv_pid import MyEnv
import torch

if __name__ == '__main__':
    env = MyEnv()
    # Read Encoders channel 0,1,2
    y = []

    for i in range(40000):
        v = 2
        v = torch.tensor([v, v])
        s_, r, done, _ = env.step(v)
        print(s_)
        #
        y += [s_[0]]
    plt.plot(y, label='e')
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.legend()
    plt.show()

import math
import time

from common.rotor_state_calculator import nonlinearheli
# from common.myenv import MyEnv
from common.myenv_simulate import MyEnv
import torch

if __name__ == '__main__':
    env = MyEnv()
    # Read Encoders channel 0,1,2
    for i in range(100):
        # v = sin(2 pi f t) ; t = i * dt(step)  f = 1Hz
        f = 1
        step = 0.1
        t = i * step
        v = math.sin(2 * math.pi * f * t) * 3
        v = torch.tensor([v, v])
        s_, r, done, _ = env.step(v)
        print(s_)
        time.sleep(0.1)
    env.reset()


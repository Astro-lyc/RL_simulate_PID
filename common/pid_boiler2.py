#!/usr/bin/env python

import time
import matplotlib.pyplot as plt
import torch
from simple_pid import PID
from myenv_pid import MyEnv


class WaterBoiler:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """

    def __init__(self):
        self.env = MyEnv()
        self.water_temp = self.env.final_state[0]  # 这个代表垂直距离
        self.v = 0  # 这个代表当前电压
        self.done = False

    def update(self, boiler_power, dt):
        # if boiler_power > 0:
        # Boiler can only produce heat, not cold
        self.v += 1 * boiler_power * dt
        if self.v > 3:
            self.v = 3
        if self.v < 0:
            self.v = 0
        # self.v = 2
        last_observation, reward, done, _ = self.env.step(torch.tensor([self.v, self.v]))
        if done:
            print('结束')
            self.done = True
            # quit()
        self.water_temp = last_observation[0]
        print('distance:  ', self.water_temp)
        print('v:   ', self.v)
        print('power:   ', boiler_power)

        # Some heat dissipation
        # self.water_temp -= 0.02 * dt
        return self.water_temp


if __name__ == '__main__':
    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    pid = PID(1, .1, 5, setpoint=water_temp, sample_time=0.0001)
    pid.output_limits = (-5, 5)

    #
    # pid2 = PID(.2, 0, 6, setpoint=water_temp, sample_time=None, auto_mode=True)
    # pid2.output_limits = (-3, 3)

    start_time = time.time()
    last_time = start_time

    # Keep track of values for plotting
    setpoint, y, x, z, p = [], [], [], [], []

    step = 1
    while time.time() - start_time < 10:
        # while not boiler.done:
        step += 1
        current_time = time.time()
        dt = current_time - last_time

        # if step % 100 == 0:
        #     pid = pid2

        power = pid(water_temp)
        # water_temp = boiler.update(power, dt)
        # water_temp = boiler.update(power, 0.1)
        water_temp = boiler.update(power, 0.005)
        # time.sleep(0.05)

        x += [current_time - start_time]
        y += [water_temp]
        p += [power]
        z += [boiler.v]
        setpoint += [pid.setpoint]

        # if current_time - start_time > 1:
        #     pid.setpoint = 100

        last_time = current_time

    # plt.plot(x, y, label='measured')
    # plt.plot(x, z, label='v')
    # plt.plot(x, setpoint, label='target')
    plt.plot(y, label='measured')
    plt.plot(z, label='v')
    plt.plot(p, label='power')
    plt.plot(setpoint, label='target')
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.legend()
    plt.show()

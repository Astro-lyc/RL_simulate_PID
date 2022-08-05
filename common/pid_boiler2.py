#!/usr/bin/env python

import time
import matplotlib.pyplot as plt
import torch
from simple_pid import PID
from myenv import MyEnv


class WaterBoiler:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """

    def __init__(self):
        self.env = MyEnv()
        self.water_temp = self.env.final_state[0]  # 这个代表垂直距离
        self.v = 0  # 这个代表当前电压

    def update(self, boiler_power, dt):
        # if boiler_power > 0:
        # Boiler can only produce heat, not cold
        self.v += 1 * boiler_power * dt
        last_observation, reward, done, _ = self.env.step(torch.tensor([self.v, self.v]))
        self.water_temp = last_observation[0]
        print(self.water_temp)

        # Some heat dissipation
        # self.water_temp -= 0.02 * dt
        return self.water_temp


if __name__ == '__main__':
    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    pid = PID(0.0005, 0.01, 0.01, setpoint=water_temp)
    pid.output_limits = (-24, 24)

    start_time = time.time()
    last_time = start_time

    # Keep track of values for plotting
    setpoint, y, x = [], [], []

    while time.time() - start_time < 10:
        current_time = time.time()
        dt = current_time - last_time

        power = pid(water_temp)
        # water_temp = boiler.update(power, dt)
        water_temp = boiler.update(power, 0.1)

        x += [current_time - start_time]
        y += [water_temp]
        setpoint += [pid.setpoint]

        # if current_time - start_time > 1:
        #     pid.setpoint = 100

        last_time = current_time

    plt.plot(x, y, label='measured')
    plt.plot(x, setpoint, label='target')
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.legend()
    plt.show()

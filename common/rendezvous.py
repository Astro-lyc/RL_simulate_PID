import numpy as np
import pip install theano
import theano.tensor as T
import matplotlib.pyplot as plt

from ilqr import iLQR
from ilqr.cost import QRCost
from ilqr.dynamics import AutoDiffDynamics


def on_iteration(iteration_count, xs, us, J_opt, accepted, converged):
    J_hist.append(J_opt)
    info = "converged" if converged else ("accepted" if accepted else "failed")
    print("iteration", iteration_count, info, J_opt)

x_inputs = [
    T.dscalar("x_0"),
    T.dscalar("y_0"),
    T.dscalar("x_1"),
    T.dscalar("y_1"),
    T.dscalar("x_0_dot"),
    T.dscalar("y_0_dot"),
    T.dscalar("x_1_dot"),
    T.dscalar("y_1_dot"),
]

u_inputs = [
    T.dscalar("F_x_0"),
    T.dscalar("F_y_0"),
    T.dscalar("F_x_1"),
    T.dscalar("F_y_1"),
]

dt = 0.1  # Discrete time step.
m = 1.0  # Mass.
alpha = 0.1  # Friction coefficient.

# Acceleration.
def acceleration(x_dot, u):
    x_dot_dot = x_dot * (1 - alpha * dt / m) + u * dt / m
    return x_dot_dot

# Discrete dynamics model definition.
f = T.stack([
    x_inputs[0] + x_inputs[4] * dt,
    x_inputs[1] + x_inputs[5] * dt,
    x_inputs[2] + x_inputs[6] * dt,
    x_inputs[3] + x_inputs[7] * dt,
    x_inputs[4] + acceleration(x_inputs[4], u_inputs[0]) * dt,
    x_inputs[5] + acceleration(x_inputs[5], u_inputs[1]) * dt,
    x_inputs[6] + acceleration(x_inputs[6], u_inputs[2]) * dt,
    x_inputs[7] + acceleration(x_inputs[7], u_inputs[3]) * dt,
])

dynamics = AutoDiffDynamics(f, x_inputs, u_inputs)


Q = np.eye(dynamics.state_size)
Q[0, 2] = Q[2, 0] = -1
Q[1, 3] = Q[3, 1] = -1
R = 0.1 * np.eye(dynamics.action_size)

cost = QRCost(Q, R)

N = 200  # Number of time steps in trajectory.
x0 = np.array([0, 0, 10, 10, 0, -5, 5, 0])  # Initial state.

# Random initial action path.
us_init = np.random.uniform(-1, 1, (N, dynamics.action_size))



J_hist = []
ilqr = iLQR(dynamics, cost, N)
xs, us = ilqr.fit(x0, us_init, on_iteration=on_iteration)


x_0 = xs[:, 0]
y_0 = xs[:, 1]
x_1 = xs[:, 2]
y_1 = xs[:, 3]
x_0_dot = xs[:, 4]
y_0_dot = xs[:, 5]
x_1_dot = xs[:, 6]
y_1_dot = xs[:, 7]





_ = plt.title("Trajectory of the two omnidirectional vehicles")
_ = plt.plot(x_0, y_0, "r")
_ = plt.plot(x_1, y_1, "b")
_ = plt.legend(["Vehicle 1", "Vehicle 2"])


t = np.arange(N + 1) * dt
_ = plt.plot(t, x_0, "r")
_ = plt.plot(t, x_1, "b")
_ = plt.xlabel("Time (s)")
_ = plt.ylabel("x (m)")
_ = plt.title("X positional paths")
_ = plt.legend(["Vehicle 1", "Vehicle 2"])


_ = plt.plot(t, y_0, "r")
_ = plt.plot(t, y_1, "b")
_ = plt.xlabel("Time (s)")
_ = plt.ylabel("y (m)")
_ = plt.title("Y positional paths")
_ = plt.legend(["Vehicle 1", "Vehicle 2"])


_ = plt.plot(t, x_0_dot, "r")
_ = plt.plot(t, x_1_dot, "b")
_ = plt.xlabel("Time (s)")
_ = plt.ylabel("x_dot (m)")
_ = plt.title("X velocity paths")
_ = plt.legend(["Vehicle 1", "Vehicle 2"])


_ = plt.plot(t, y_0_dot, "r")
_ = plt.plot(t, y_1_dot, "b")
_ = plt.xlabel("Time (s)")
_ = plt.ylabel("y_dot (m)")
_ = plt.title("Y velocity paths")
_ = plt.legend(["Vehicle 1", "Vehicle 2"])


_ = plt.plot(J_hist)
_ = plt.xlabel("Iteration")
_ = plt.ylabel("Total cost")
_ = plt.title("Total cost-to-go")

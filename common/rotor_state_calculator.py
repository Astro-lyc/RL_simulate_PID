import math

'''旋翼装置状态计算器'''


def nonlinearheli(X, U):
    # Propeller force-thrust constant found experimentally (N/V)
    Kf = 0.1188
    # Mass of the helicopter body (kg)
    mh = 1.308
    # Mass of counter-weight (kg)
    mw = 1.924
    # Mass of front propeller assembly = motor + shield + propeller + body (kg)
    mf = mh / 2
    # Mass of back propeller assembly = motor + shield + propeller + body (kg)
    mb = mh / 2
    # Distance between pitch pivot and each motor (m)
    Lh = 7.0 * 0.0254
    # Distance between elevation pivot to helicopter body (m)
    La = 26.0 * 0.0254
    # Distance between elevation pivot to counter-weight (m)
    Lw = 18.5 * 0.0254
    # Gravitational Constant (m/s^2)
    g = 9.81
    # TODO 三个角速度
    epsilon_dot = X[3]  # eps 上下
    rho_dot = X[4]  # rou 角速度
    lambda_dot = X[5]  # 左右 角速度
    # TODO 三个加速度

    # X[1] 换成
    epsilon_ddot = -math.cos(X[1]) ** 2 * Lh * (mf - mb) * La * math.sin(X[1]) / (
            (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[3] ** 2 + (
                           -2 * Lh * math.cos(X[1]) * (
                           math.cos(X[0]) * La * (mf - mb) * math.cos(X[1]) ** 2 - math.cos(X[0]) * La * (
                           mf - mb) + math.sin(X[1]) * math.sin(X[0]) * Lh * (mf + mb)) / (
                                   (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * Lh * X[
                               5] - 2 * (mf + mb) * math.cos(X[1]) * Lh ** 2 * math.sin(X[1]) * X[4] / (
                                   (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw)) * X[3] + (
                           (math.sin(X[1]) * La * (mf - mb) * math.cos(X[0]) - 2 * math.sin(X[0]) * Lh * (
                                   mf + mb)) * Lh * math.cos(X[0]) * math.cos(X[1]) ** 2 - 2 * math.sin(
                       X[1]) * La * Lh * (mf - mb) * math.cos(X[0]) ** 2 - math.sin(X[0]) * (
                                   (mf + mb) * La ** 2 - Lh ** 2 * mb - Lh ** 2 * mf + Lw ** 2 * mw) * math.cos(
                       X[0]) + math.sin(X[1]) * La * Lh * (mf - mb)) / (
                           (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[
                       5] ** 2 - 2 * Lh * (
                           math.cos(X[0]) * Lh * (mf + mb) * math.cos(X[1]) ** 2 - math.cos(X[0]) * Lh * (
                           mf + mb) - math.sin(X[1]) * math.sin(X[0]) * La * (mf - mb)) * X[4] / (
                           (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[5] + Lh * (
                           mf - mb) * La * math.sin(X[1]) / (
                           (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[4] ** 2 + (
                           ((g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g) * (
                           (mf - mb) ** 2 * La ** 2 + Lh ** 2 * (mf + mb) ** 2) * math.cos(X[1]) ** 3 + (g * (
                           mw * Lw * (mf - mb) ** 2 * La ** 2 + (
                           (-0.4e1 * Lh ** 2 * mf + Lw ** 2 * mw) * mb ** 2 + (
                           -0.4e1 * Lh ** 2 * mf ** 2 - 0.2e1 * Lw ** 2 * mw * mf) * mb + mf ** 2 * mw * Lw ** 2) * La + mw * Lh ** 2 * Lw * (
                                   mf + mb) ** 2) * math.cos(X[0]) + ((g * mb + g * mf + Kf * (
                           U[0] + U[1])) * La - Lw * mw * g) * ((mf - mb) ** 2 * La ** 2 + Lh ** 2 * (
                           mf + mb) ** 2)) * math.cos(X[0]) * math.cos(X[1]) ** 2 + (
                                   Kf * (-U[0] + U[1]) * (mf - mb) * ((
                                                                              mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * La * math.cos(
                               X[0]) - (math.sin(X[0]) * Kf * Lh * (-U[0] + U[1]) * math.sin(X[1]) + (
                                   g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g) * (
                                           (mf - mb) ** 2 * La ** 2 + Lh ** 2 * (mf + mb) ** 2)) * math.cos(
                       X[1]) + (0.4e1 * La ** 2 * mb * mf + mw * Lw ** 2 * (mf + mb)) * math.cos(X[0]) * (
                                   -g * ((mf + mb) * La - Lw * mw) * math.cos(X[0]) + g * math.sin(
                               X[0]) * Lh * (mf - mb) * math.sin(X[1]) + (
                                           g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g)) / (
                           0.4e1 * La ** 2 * mb * mf + mw * Lw ** 2 * (mf + mb)) / (
                           (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) / math.cos(X[0])
    rho_ddot = math.cos(X[1]) * (
            ((mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * math.sin(X[1]) * math.cos(X[0]) + math.cos(
        X[1]) ** 2 * math.sin(X[0]) * La * Lh * (mf - mb)) / math.cos(X[0]) / (
                       (mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * X[3] ** 2 + (-0.2e1 * (
            -math.cos(X[1]) ** 2 * ((mf + mb) * La ** 2 + Lw ** 2 * mw) * math.cos(X[0]) ** 2 + math.cos(
        X[1]) ** 2 * math.sin(X[1]) * math.sin(X[0]) * La * Lh * (mf - mb) * math.cos(X[0]) - Lh ** 2 * (
                    mf + mb) * math.cos(X[1]) ** 2 + (mf + mb) * Lh ** 2 + (
                    mf + mb) * La ** 2 + Lw ** 2 * mw) / math.cos(X[0]) / ((mf + mb) * Lh ** 2 + (
            mf + mb) * La ** 2 + Lw ** 2 * mw) * X[5] + 0.2e1 * (mf + mb) * math.cos(
        X[1]) ** 2 * Lh ** 2 * math.sin(X[0]) * X[4] / math.cos(X[0]) / ((mf + mb) * Lh ** 2 + (
            mf + mb) * La ** 2 + Lw ** 2 * mw)) * X[3] - math.cos(X[1]) * (
                       ((-mb - mf) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * math.sin(X[1]) * math.cos(
                   X[0]) ** 3 + math.sin(X[0]) * La * Lh * (math.cos(X[1]) ** 2 - 0.2e1) * (mf - mb) * math.cos(
                   X[0]) ** 2 + 0.2e1 * math.sin(X[1]) * Lh ** 2 * (mf + mb) * math.cos(X[0]) + math.sin(
                   X[0]) * La * Lh * (mf - mb)) / math.cos(X[0]) / (
                       (mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * X[
                   5] ** 2 - 0.2e1 * Lh * math.cos(X[1]) * (
                       -La * (mf - mb) * math.cos(X[0]) ** 2 + math.sin(X[1]) * math.sin(X[0]) * Lh * (
                       mf + mb) * math.cos(X[0]) + La * (mf - mb)) * X[4] / math.cos(X[0]) / (
                       (mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * X[5] - math.cos(
        X[1]) * Lh * math.sin(X[0]) * (mf - mb) * La / math.cos(X[0]) / (
                       (mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * X[4] ** 2 + (
                       -g * math.cos(X[1]) * (mf - mb) * (
                       (-0.4e1 * La * mb * mf + mw * Lw * (mf + mb)) * La * Lh ** 2 + Lw * (
                       (mf + mb) * La ** 2 + Lw ** 2 * mw) * (La + Lw) * mw) * math.cos(X[0]) ** 3 + (
                               -Lh ** 2 * Kf * (-U[0] + U[1]) * (
                               (mf - mb) ** 2 * La ** 2 + Lh ** 2 * (mf + mb) ** 2) * math.cos(
                           X[1]) ** 2 + (g * Lh * math.sin(X[0]) * ((mf + mb) * (
                               -0.4e1 * La * mb * mf + mw * Lw * (mf + mb)) * Lh ** 2 + Lw * La * mw * (
                                                                            mf - mb) ** 2 * (
                                                                            La + Lw)) * math.sin(X[1]) - ((
                                                                                                                  g * mb + g * mf + Kf * (
                                                                                                                  U[
                                                                                                                      0] +
                                                                                                                  U[
                                                                                                                      1])) * La - Lw * mw * g) * (
                                                 mf - mb) * ((mf + mb) * Lh ** 2 + (
                               mf + mb) * La ** 2 + Lw ** 2 * mw) * La) * math.cos(X[1]) - Kf * (
                                       -U[0] + U[1]) * (
                                       (-mb - mf) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * (
                                       (mf + mb) * Lh ** 2 + (
                                       mf + mb) * La ** 2 + Lw ** 2 * mw)) * math.cos(X[0]) ** 2 + (
                               -((g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g) * (mf - mb) * (
                               (mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) * La * math.cos(
                           X[1]) ** 2 + Lh * (((g * mb + g * mf + Kf * (
                               U[0] + U[1])) * La - Lw * mw * g) * math.sin(X[0]) * (
                                                      (mf - mb) ** 2 * La ** 2 + Lh ** 2 * (
                                                      mf + mb) ** 2) * math.sin(X[1]) - g * Lh * (
                                                      0.4e1 * La ** 2 * mb * mf + mw * Lw ** 2 * (
                                                      mf + mb)) * (mf - mb)) * math.cos(X[1]) + (
                                       0.2e1 * math.sin(X[0]) * Kf * Lh * (-U[0] + U[1]) * math.sin(
                                   X[1]) + (g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g) * (
                                       mf - mb) * ((mf + mb) * Lh ** 2 + (
                               mf + mb) * La ** 2 + Lw ** 2 * mw) * La) * math.cos(X[0]) + Lh * (
                               ((g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g) * math.sin(
                           X[0]) * math.sin(X[1]) + Kf * Lh * (-U[0] + U[1])) * (
                               ((mf - mb) ** 2 * La ** 2 + Lh ** 2 * (mf + mb) ** 2) * math.cos(X[1]) ** 2 - (
                               mf + mb) * (
                                       (mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw))) / Lh / (
                       0.4e1 * La ** 2 * mb * mf + mw * Lw ** 2 * (mf + mb)) / (
                       (mf + mb) * Lh ** 2 + (mf + mb) * La ** 2 + Lw ** 2 * mw) / math.cos(X[0]) ** 2
    lambda_ddot = -math.cos(X[1]) ** 3 * Lh * (mf - mb) * La / math.cos(X[0]) / (
            (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[3] ** 2 + (0.2e1 * (
            Lh * (math.sin(X[1]) * La * (mf - mb) * math.cos(X[0]) - math.sin(X[0]) * Lh * (mf + mb)) * math.cos(
        X[1]) ** 2 + math.sin(X[0]) * (
                    (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw)) / math.cos(X[0]) / ((
                                                                                                                   mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) *
                                                                                             X[5] - 0.2e1 * (
                                                                                                     mf + mb) * math.cos(
                X[1]) ** 2 * Lh ** 2 * X[4] / math.cos(X[0]) / ((
                                                                        mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw)) * \
                  X[3] + math.cos(X[1]) * Lh * (
                          La * (mf - mb) * math.cos(X[0]) ** 2 * math.cos(X[1]) ** 2 + 0.2e1 * math.sin(
                      X[1]) * math.sin(X[0]) * Lh * (mf + mb) * math.cos(X[0]) - 0.2e1 * (mf - mb) * (
                                  math.cos(X[0]) ** 2 - 0.1e1 / 0.2e1) * La) / math.cos(X[0]) / (
                          (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[5] ** 2 + 0.2e1 * (
                          math.cos(X[0]) * Lh * (mf + mb) * math.sin(X[1]) + math.sin(X[0]) * La * (
                          mf - mb)) * math.cos(X[1]) * Lh * X[4] / math.cos(X[0]) / (
                          (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[5] + math.cos(
        X[1]) * Lh * (mf - mb) * La / math.cos(X[0]) / (
                          (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) * X[4] ** 2 + (-(
            ((g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g) * math.sin(X[1]) + math.sin(
        X[0]) * Kf * Lh * (-U[0] + U[1])) * ((mf - mb) ** 2 * La ** 2 + Lh ** 2 * (mf + mb) ** 2) * math.cos(
        X[1]) ** 2 - ((g * (mw * Lw * (mf - mb) ** 2 * La ** 2 + ((-0.4e1 * Lh ** 2 * mf + Lw ** 2 * mw) * mb ** 2 + (
            -0.4e1 * Lh ** 2 * mf ** 2 - 0.2e1 * Lw ** 2 * mw * mf) * mb + mf ** 2 * mw * Lw ** 2) * La + mw * Lh ** 2 * Lw * (
                                    mf + mb) ** 2) * math.cos(X[0]) + (
                               (g * mb + g * mf + Kf * (U[0] + U[1])) * La - Lw * mw * g) * (
                               (mf - mb) ** 2 * La ** 2 + Lh ** 2 * (mf + mb) ** 2)) * math.sin(
        X[1]) - g * Lh * math.sin(X[0]) * (0.4e1 * La ** 2 * mb * mf + mw * Lw ** 2 * (mf + mb)) * (
                              mf - mb)) * math.cos(X[0]) * math.cos(X[1]) + ((-Kf * La * (-U[0] + U[1]) * (
            mf - mb) * math.cos(X[0]) + (mf + mb) * ((g * mb + g * mf + Kf * (
            U[0] + U[1])) * La - Lw * mw * g)) * math.sin(X[1]) + math.sin(X[0]) * Kf * Lh * (-U[0] + U[1]) * (
                                                                                     mf + mb)) * ((
                                                                                                          mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw)) / (
                          0.4e1 * La ** 2 * mb * mf + mw * Lw ** 2 * (mf + mb)) / (
                          (mf + mb) * La ** 2 + Lh ** 2 * mb + Lh ** 2 * mf + Lw ** 2 * mw) / math.cos(X[0]) ** 2

    DERX = [X[3], X[4], X[5], epsilon_ddot, rho_ddot, lambda_ddot]
    # todo 前三个是什么值？为什么把DERX*0.1直接加到Y上？如何判断失败？
    Y = [X[0], X[1], X[2], epsilon_dot, rho_dot, lambda_dot]
    return Y, DERX


# 装置的下一个状态计算：输入的6个状态 -> 下一个的6个状态
def device_next_state(Y, U):
    Y, DERX = nonlinearheli(Y, U)
    # Y = Y + DERX * h; % h =0.1
    timestep = 0.1
    Y = [it2 + Y[i] for i, it2 in enumerate([item * timestep for item in DERX])]
    return Y


if __name__ == '__main__':
    U = [1, 1]  # 电压 ：-10,10
    # X = [-15 / 180 * 3.1415, 0, 0, 0, 0, 0]  # 初始状态
    # Y = [-15 / 180 * 3.1415, 0, 0, 0, 0, 0]  # 初始状态
    Y = [.0, .0, .0, .0, .0, .0]  # 初始状态
    timestep = 0.1

    Y = [0.0, 0.0, 0.0, 0.015744473003389235, 0.010652038204937033, 0.0]
    U = [1.1029335260391235, 0.8944096565246582]

    for i in range(1):
        Y, DERX = nonlinearheli(Y, U)
        # Y = Y + DERX * h; % h =0.1
        Y = [it2 + Y[i] for i, it2 in enumerate([item * timestep for item in DERX])]
        print(Y)

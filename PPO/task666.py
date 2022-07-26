import sys, os

curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径

# import gym
from common.myenv import MyEnv
import torch
import datetime
from common.utils import plot_rewards
from common.utils import save_results, make_dir
from ppo2 import PPO

curr_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")  # 获取当前时间


class PPOConfig:
    def __init__(self) -> None:
        self.algo = "PPO"  # 算法名称
        self.env_name = 'RL_simulate_PID'  # 环境名称
        self.continuous = True  # 环境是否为连续动作
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 检测GPU
        self.train_eps = 200  # 训练的回合数
        self.test_eps = 20  # 测试的回合数
        self.batch_size = 5
        self.gamma = 0.99
        self.n_epochs = 4
        self.actor_lr = 0.0003
        self.critic_lr = 0.0003
        self.gae_lambda = 0.95
        self.policy_clip = 0.2
        self.hidden_dim = 256
        self.update_fre = 20  # frequency of agent update


class PlotConfig:
    def __init__(self) -> None:
        self.algo = "PPO"  # 算法名称
        self.env_name = 'RL_simulate_PID'  # 环境名称
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 检测GPU
        self.result_path = curr_path + "/outputs/" + self.env_name + \
                           '/' + curr_time + '/results/'  # 保存结果的路径
        self.model_path = curr_path + "/outputs/" + self.env_name + \
                          '/' + curr_time + '/models/'  # 保存模型的路径
        self.save = True  # 是否保存图片


def env_agent_config(cfg, seed=1):
    env = MyEnv()
    env.seed(seed)
    n_states = env.observation_space.shape[0]
    n_actions = env.action_space.shape[0]
    agent = PPO(n_states, n_actions, cfg)
    return env, agent


def train(cfg, env, agent):
    print('开始训练！')
    print(f'环境：{cfg.env_name}, 算法：{cfg.algo}, 设备：{cfg.device}')
    rewards = []  # 记录所有回合的奖励
    ma_rewards = []  # 记录所有回合的滑动平均奖励
    steps = 0
    for i_ep in range(cfg.train_eps):
        state = env.reset()
        done = False
        ep_reward = 0
        while not done:
            action, prob, val = agent.choose_action(state)
            state_, reward, done, _ = env.step(action)
            steps += 1
            ep_reward += reward
            agent.memory.push(state, action, prob, val, reward, done)
            if steps % cfg.update_fre == 0:
                agent.update()
            state = state_
        rewards.append(ep_reward)
        if ma_rewards:
            ma_rewards.append(0.9 * ma_rewards[-1] + 0.1 * ep_reward)
        else:
            ma_rewards.append(ep_reward)
        if (i_ep + 1) % 10 == 0:
            print(f"回合：{i_ep + 1}/{cfg.train_eps}，奖励：{ep_reward:.2f}")
    print('完成训练！')
    return rewards, ma_rewards


if __name__ == '__main__':
    cfg = PPOConfig()
    plot_cfg = PlotConfig()
    # 训练
    env, agent = env_agent_config(cfg, seed=1)
    rewards, ma_rewards = train(cfg, env, agent)
    make_dir(plot_cfg.result_path, plot_cfg.model_path)  # 创建保存结果和模型路径的文件夹
    agent.save(path=plot_cfg.model_path)
    save_results(rewards, ma_rewards, tag='train', path=plot_cfg.result_path)
    plot_rewards(rewards, ma_rewards, plot_cfg, tag="train")
    # 测试
    # env,agent = env_agent_config(cfg,seed=10)
    # agent.load(path=plot_cfg.model_path)
    # rewards,ma_rewards = eval(cfg,env,agent)
    # save_results(rewards,ma_rewards,tag='eval',path=plot_cfg.result_path)
    # plot_rewards(rewards, ma_rewards, plot_cfg, tag="eval")

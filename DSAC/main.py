import numpy as np
import torch

# import gym
from DSAC import DSAC_Agent
from ReplayBuffer import RandomBuffer, device
# from torch.utils.tensorboard import SummaryWriter
# from datetime import datetime
import os, shutil
import argparse
from Adapter import *
from Cat import Cat

# 包含psi
def str2bool(v):
    '''transfer str to bool for argparse'''
    '''yes', 'True','true','TRUE', 't', 'y' they all mean true '''
    ''''no', 'False','false','FALSE', 'f', 'n', '0' they all mean false '''
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'True', 'true', 'TRUE', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'False', 'false', 'FALSE', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


'''Hyperparameter Setting''' # 超参数 （一般就是根据经验确定的变量） 在深度学习中，超参数有：学习速率，迭代次数，层数，每层神经元的个数等等。
parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default='', help='save path')
parser.add_argument('--EnvIdex', type=int, default=0)
parser.add_argument('--write', type=str2bool, default=True, help='Use SummaryWriter to record the training')
parser.add_argument('--render', type=str2bool, default=False, help='Render or Not')
parser.add_argument('--Loadmodel', type=str2bool, default=False, help='Load pretrained model or Not')
parser.add_argument('--ModelIdex', type=int, default=10000, help='which model to load')
parser.add_argument('--seed', type=int, default=1, help='random seed')

parser.add_argument('--total_steps', type=int, default=int(5e6), help='Max training steps')
parser.add_argument('--save_interval', type=int, default=int(4e3), help='Model saving interval, in steps.')
parser.add_argument('--eval_interval', type=int, default=int(4e3), help='Model evaluating interval, in stpes.')
parser.add_argument('--eval_turn', type=int, default=1, help='Model evaluating times, in episode.')
parser.add_argument('--update_every', type=int, default=50, help='Training Fraquency, in stpes')
parser.add_argument('--gamma', type=float, default=0.99, help='Discounted Factor')
parser.add_argument('--net_width', type=int, default=256, help='Hidden net width')
parser.add_argument('--a_lr', type=float, default=3e-4, help='Learning rate of actor')
parser.add_argument('--c_lr', type=float, default=3e-4, help='Learning rate of critic')
parser.add_argument('--batch_size', type=int, default=256, help='Batch Size')
parser.add_argument('--alpha', type=float, default=0.12, help='Entropy coefficient')
parser.add_argument('--adaptive_alpha', type=str2bool, default=True, help='Use adaptive_alpha or Not')

parser.add_argument('--boat_state_bound', type=list, default=[200, 200, 10], help='Bound of state')
parser.add_argument('--boat_action_bound', type=list, default=np.array([2, 1.5, 1.5]), help='Bound of action')
parser.add_argument('--break_reward', type=float, default=-50000, help='Reward bound')
parser.add_argument('--boat_plot', type=str2bool, default=True, help='Plot or not')
opt = parser.parse_args()
print(opt)
parser.add_argument('--boat_time_seq', type=list, default=np.linspace(0, 80, 4000), help='Time seq')
opt = parser.parse_args()


def evaluate_policy(env, model, render, steps_per_epoch, max_action, EnvIdex):
    scores = 0
    turns = opt.eval_turn
    for j in range(turns):
        s, done, ep_r = env.reset(), False, 0
        if opt.EnvIdex==6 and opt.boat_plot:
            env.draw(1)
        while not done:
            # Take deterministic actions at test time
            a = model.select_action(s, deterministic=True, with_logprob=False)
            act = Action_adapter(a, max_action)  # [0,1] to [-max,max]
            s_prime, r, done, info = env.step(act)
            # r = Reward_adapter(r, EnvIdex)
            ep_r += r
            s = s_prime
            if render:
                env.render()
        if opt.EnvIdex==6 and opt.boat_plot:
                env.draw(0)
        ep_r=ep_r/env.step_time
        # print(ep_r)
        scores += ep_r
    return scores / turns*100


def main():
    write = opt.write  # Use SummaryWriter to record the training.
    render = opt.render
    EnvName = ['Cat']
    Env_With_Dead = [True, True, True, False, True, False, True]
    EnvIdex = opt.EnvIdex
    env_with_Dead = Env_With_Dead[EnvIdex]
    if EnvName[EnvIdex] == 'Cat':
        env = Cat(time_step=opt.boat_time_seq, state_bound=opt.boat_state_bound,
                   action_bound=opt.boat_action_bound, break_reward=opt.break_reward)
        eval_env = Cat(time_step=opt.boat_time_seq, state_bound=opt.boat_state_bound,
                        action_bound=opt.boat_action_bound, break_reward=opt.break_reward)
        state_dim = env.observation.shape[0]
        action_dim = env.action_space.shape[0]
        max_action = opt.boat_action_bound
        min_action = float(-env.action_bound[0])
        steps_per_epoch = env.max_step

        start_steps = 5 * steps_per_epoch  # in steps
        update_after = 2 * steps_per_epoch  # in steps
        update_every = opt.update_every  # Training Frequency, in steps
        total_steps = opt.total_steps  # Max training steps
        eval_interval = opt.eval_interval  # in steps
        save_interval = opt.save_interval  # in steps

        random_seed = opt.seed
        print("Random Seed: {}".format(random_seed))
        torch.manual_seed(random_seed)
        env.seed(random_seed)
        eval_env.seed(random_seed)
        np.random.seed(random_seed)

        kwargs = {
            "state_dim": state_dim,
            "action_dim": action_dim,
            "gamma": opt.gamma,  # discount factor
            "hid_shape": (opt.net_width, opt.net_width),
            "a_lr": opt.a_lr,  # actor learning rate
            "c_lr": opt.c_lr,  # critic and alpha learning rate
            "batch_size": opt.batch_size,
            "alpha": opt.alpha,
            "adaptive_alpha": opt.adaptive_alpha
        }


        model = DSAC_Agent(**kwargs)
        if not os.path.exists('model'): os.mkdir('model')
        if opt.Loadmodel: model.load(opt.ModelIdex)

        replay_buffer = RandomBuffer(state_dim, action_dim, env_with_Dead, dir_path=opt.path, max_size=int(1e6))

        if render:
            average_reward = evaluate_policy(env, model, render, steps_per_epoch, max_action, EnvIdex)
            print('Average Reward:', average_reward)
        else:
            s, done, current_steps = env.reset(), False, 0
            for t in range(total_steps):  # Max training steps' default as 1e6
                current_steps += 1
                '''Interact & trian'''
                if t < start_steps:  # when to start using model: default as 5 * steps_per_epoch
                    # Random explore for start_steps
                    if EnvName[EnvIdex] == 'Cat':
                        act = env.sample()  # act∈[-max,max]
                        a = Action_adapter_reverse(act, max_action)  # a∈[-1,1]
                    else:
                        act = env.action_space.sample()  # act∈[-max,max]
                        a = Action_adapter_reverse(act, max_action)  # a∈[-1,1]
                else:
                    a = model.select_action(s, deterministic=False, with_logprob=False)  # a∈[-1,1]
                    act = Action_adapter(a, max_action)  # act∈[-max,max]
                s_prime, r, done, info = env.step(act)
                dead = Done_adapter(r, done, current_steps, EnvIdex,opt.break_reward)
                r = Reward_adapter(r, EnvIdex,opt.break_reward)
                replay_buffer.add(s, a, r, s_prime, dead)
                s = s_prime
                # 50 environment steps company with 50 gradient steps.
                # Stabler than 1 environment step company with 1 gradient step.
                if t >= update_after and t % update_every == 0:
                    # update_after default as 2 * steps_per_epoch
                    # update_every is the training frequency default as 50
                    for j in range(update_every):
                        model.train(replay_buffer)
                '''save model'''
                if (t + 1) % save_interval == 0:
                    print('save model')
                    model.save(t + 1)

                '''record & log'''
                if (t + 1) % eval_interval == 0:
                    score = evaluate_policy(eval_env, model, opt.render, steps_per_epoch, max_action, EnvIdex)
                    # if write:
                    #     writer.add_scalar('ep_r', score, global_step=t + 1)
                    #     writer.add_scalar('alpha', model.alpha, global_step=t + 1)
                    print('\nEnvName:', EnvName[EnvIdex], 'seed:', random_seed, 'totalsteps:', t + 1, 'score:', score)
                if done:
                    s, done, current_steps = env.reset(), False, 0

        env.close()
        eval_env.close()


if __name__ == '__main__':
    main()

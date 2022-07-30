import loguru
import torch
import numpy as np
from torch.utils.tensorboard import SummaryWriter
# import gym
# from common.myenv_simulate import MyEnv
from common.myenv import MyEnv

import argparse
from normalization import Normalization, RewardScaling
from replaybuffer import ReplayBuffer
from ppo_continuous import PPO_continuous


def evaluate_policy(args, env, agent, state_norm):
    times = 3
    evaluate_reward = 0
    hand_on_step = 0  # 新增：总的
    for _ in range(times):
        # todo re_list = []
        s = env.reset()
        if args.use_state_norm:
            s = state_norm(s, update=False)  # During the evaluating,update=False
        done = False
        episode_reward = 0
        step = 0  # 新增：每回合坚持回合数
        while not done:
            a = agent.evaluate(s)  # We use the deterministic policy during the evaluating
            if args.policy_dist == "Beta":
                action = 2 * (a - 0.5) * args.max_action  # [0,1]->[-max,max]
            else:
                action = a
            s_, r, done, _ = env.step(action)
            # todo append
            if args.use_state_norm:
                s_ = state_norm(s_, update=False)
            episode_reward += r
            s = s_
            step += 1
        hand_on_step += step
        evaluate_reward += episode_reward
        # todo 画图 plt.save
    # 新增：平均每回合坚持step数量
    return evaluate_reward / times, hand_on_step / times


def main(args, env_name, number, seed):
    # env = gym.make(env_name)
    env = MyEnv()
    # env_evaluate = gym.make(env_name)  # When evaluating the policy, we need to rebuild an environment
    # env_evaluate = MyEnv()  # When evaluating the policy, we need to rebuild an environment
    env_evaluate = env  # When evaluating the policy, we need to rebuild an environment
    # Set random seed
    env.seed(seed)
    # env.action_space.seed(seed)
    env_evaluate.seed(seed)
    # env_evaluate.action_space.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    args.state_dim = env.observation_space.shape[0]
    args.action_dim = env.action_space.shape[0]
    # fixme 10？
    # args.max_action = float(env.action_space.high[0])
    args.max_action = 24.0
    # args.max_episode_steps = env._max_episode_steps  # Maximum number of steps per episode
    args.max_episode_steps = 2000  # Maximum number of steps per episode
    print("env={}".format(env_name))
    print("state_dim={}".format(args.state_dim))
    print("action_dim={}".format(args.action_dim))
    print("max_action={}".format(args.max_action))
    print("max_episode_steps={}".format(args.max_episode_steps))

    evaluate_num = 0  # Record the number of evaluations
    evaluate_rewards = []  # Record the rewards during the evaluating
    total_steps = 0  # Record the total steps during the training

    replay_buffer = ReplayBuffer(args)
    agent = PPO_continuous(args)

    # Build a tensorboard
    writer = SummaryWriter(
        log_dir='runs/PPO_continuous/env_{}_{}_number_{}_seed_{}_4'.format(env_name, args.policy_dist, number, seed))

    state_norm = Normalization(shape=args.state_dim)  # Trick 2:state normalization
    if args.use_reward_norm:  # Trick 3:reward normalization
        reward_norm = Normalization(shape=1)
    elif args.use_reward_scaling:  # Trick 4:reward scaling
        reward_scaling = RewardScaling(shape=1, gamma=args.gamma)

    while total_steps < args.max_train_steps:
        s = env.reset()
        if args.use_state_norm:
            s = state_norm(s)
        if args.use_reward_scaling:
            reward_scaling.reset()
        episode_steps = 0
        done = False
        while not done:
            episode_steps += 1
            a, a_logprob = agent.choose_action(s)  # Action and the corresponding log probability
            if args.policy_dist == "Beta":
                action = 2 * (a - 0.5) * args.max_action  # [0,1]->[-max,max]
            else:
                action = a
            s_, r, done, _ = env.step(action)
            if episode_steps % 30 == 0:
                print('s:', s_, 'a:', a, 'r:', r)
                # print(s)
                # print(a)
                # print(r)
            if args.use_state_norm:
                s_ = state_norm(s_)
            if args.use_reward_norm:
                r = reward_norm(r)
            elif args.use_reward_scaling:
                r = reward_scaling(r)

            # When dead or win or reaching the max_episode_steps, done will be Ture, we need to distinguish them;
            # dw means dead or win,there is no next state s';
            # but when reaching the max_episode_steps,there is a next state s' actually.
            if done and episode_steps != args.max_episode_steps:
                dw = True
            else:
                dw = False

            # Take the 'action'，but store the original 'a'（especially for Beta）
            replay_buffer.store(s, a, a_logprob, r, s_, dw, done)
            s = s_
            total_steps += 1

            # When the number of transitions in buffer reaches batch_size,then update
            if replay_buffer.count == args.batch_size:
                lr_a, lr_c, loss = agent.update(replay_buffer, total_steps)  # 两个学习率也记录一下
                writer.add_scalar('LR/lr_a_{}'.format(env_name), lr_a, global_step=total_steps)
                writer.add_scalar('LR/lr_c_{}'.format(env_name), lr_c, global_step=total_steps)
                writer.add_scalar('Loss/loss_{}'.format(env_name), loss, global_step=total_steps)
                writer.add_scalar('Reword/last_reward_{}'.format(env_name), r, global_step=total_steps)
                # U
                writer.add_scalar('U/left', a[0], global_step=total_steps)
                writer.add_scalar('U/right', a[1], global_step=total_steps)
                # S
                writer.add_scalar('State/epi', s[0], global_step=total_steps)
                writer.add_scalar('State/rou', s[1], global_step=total_steps)
                writer.add_scalar('State/lam', s[2], global_step=total_steps)
                #
                writer.add_scalar('StateDot/epi_dot', s[3], global_step=total_steps)
                writer.add_scalar('StateDot/rou_dot', s[4], global_step=total_steps)
                writer.add_scalar('StateDot/lam_dot', s[5], global_step=total_steps)
                replay_buffer.count = 0

            # Evaluate the policy every 'evaluate_freq' steps
            if total_steps % args.evaluate_freq == 0:
                loguru.logger.info("当前total_steps：{}", total_steps)
                evaluate_num += 1
                evaluate_reward, hand_on_steps = evaluate_policy(args, env_evaluate, agent, state_norm)
                evaluate_rewards.append(evaluate_reward)
                print("evaluate_num:{} \t evaluate_reward:{} \t".format(evaluate_num, evaluate_reward))
                writer.add_scalar('step_rewards_{}'.format(env_name), evaluate_rewards[-1], global_step=total_steps)
                writer.add_scalar('hold_on_steps_{}'.format(env_name), hand_on_steps, global_step=total_steps)
                # Save the rewards
                if evaluate_num % args.save_freq == 0:
                    np.save(
                        './data_train/PPO_continuous_{}_env_{}_number_{}_seed_{}.npy'.format(args.policy_dist, env_name,
                                                                                             number, seed),
                        np.array(evaluate_rewards))
                    # 保存模型v -> 只存个actor就行了
                    if evaluate_rewards[-1] > evaluate_rewards[-2] and total_steps > 80 * 1e3:
                        torch.save(agent.actor.state_dict(),
                                   './PPO_actor_newest.pth')  # 保存权重少了state_dict智障行为
                        loguru.logger.warning("已保存权重！")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Hyperparameters Setting for PPO-continuous")
    parser.add_argument("--max_train_steps", type=int, default=int(3e6), help=" Maximum number of training steps")
    parser.add_argument("--evaluate_freq", type=float, default=5e3,
                        help="Evaluate the policy every 'evaluate_freq' steps")
    parser.add_argument("--save_freq", type=int, default=20, help="Save frequency")
    parser.add_argument("--policy_dist", type=str, default="Gaussian", help="Beta or Gaussian")
    parser.add_argument("--batch_size", type=int, default=2048, help="Batch size")
    parser.add_argument("--mini_batch_size", type=int, default=64, help="Minibatch size")
    parser.add_argument("--hidden_width", type=int, default=64,
                        help="The number of neurons in hidden layers of the neural network")
    parser.add_argument("--lr_a", type=float, default=3e-4, help="Learning rate of actor")
    parser.add_argument("--lr_c", type=float, default=3e-4, help="Learning rate of critic")
    parser.add_argument("--gamma", type=float, default=0.99, help="Discount factor")
    parser.add_argument("--lamda", type=float, default=0.95, help="GAE parameter")
    parser.add_argument("--epsilon", type=float, default=0.2, help="PPO clip parameter")
    parser.add_argument("--K_epochs", type=int, default=10, help="PPO parameter")
    parser.add_argument("--use_adv_norm", type=bool, default=True, help="Trick 1:advantage normalization")
    parser.add_argument("--use_state_norm", type=bool, default=True, help="Trick 2:state normalization")
    parser.add_argument("--use_reward_norm", type=bool, default=False, help="Trick 3:reward normalization")
    parser.add_argument("--use_reward_scaling", type=bool, default=True, help="Trick 4:reward scaling")
    parser.add_argument("--entropy_coef", type=float, default=0.01, help="Trick 5: policy entropy")
    parser.add_argument("--use_lr_decay", type=bool, default=True, help="Trick 6:learning rate Decay")
    parser.add_argument("--use_grad_clip", type=bool, default=True, help="Trick 7: Gradient clip")
    parser.add_argument("--use_orthogonal_init", type=bool, default=True, help="Trick 8: orthogonal initialization")
    parser.add_argument("--set_adam_eps", type=float, default=True, help="Trick 9: set Adam epsilon=1e-5")
    parser.add_argument("--use_tanh", type=float, default=True, help="Trick 10: tanh activation function")

    args = parser.parse_args()

    env_name = ['Pendulum-v1', 'BipedalWalker-v3', 'HalfCheetah-v2', 'Hopper-v2', 'Walker2d-v2']
    env_index = 0
    main(args, env_name=env_name[env_index], number=1, seed=10)

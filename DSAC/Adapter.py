def Reward_adapter(r, EnvIdex,break_reward=-100):
    # For BipedalWalker
    if EnvIdex == 0 or EnvIdex == 1:
        if r <= -100: r = -30

    # For Pendulum-v0
    elif EnvIdex==6:
        if r <= break_reward: r = break_reward
    elif EnvIdex == 3:
        r = (r + 8) / 8
    return r

def Done_adapter(r,done,current_steps, EnvIdex,break_reward=-100):
    # For BipedalWalker
    if EnvIdex == 0 or EnvIdex == 1 or EnvIdex==6:
        if r <= break_reward: Done = True
        else: Done = False
    else:
        Done = done
    return Done

def Action_adapter(a,max_action):
    #from [-1,1] to [-max,max]
    return  a*max_action

def Action_adapter_reverse(act,max_action):
    #from [-max,max] to [-1,1]
    return  act/max_action



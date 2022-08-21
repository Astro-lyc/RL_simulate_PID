# 训练
python PPO_continuous_train.py --max_train_steps 30000000 --lr_a 3e-4 --lr_c 3e-4
# 预测
python PPO_predict.py

# 监控(训练)
tensorboard --logdir /runs/PPO_continuous
# 监控(预测)
tensorboard --logdir /runs/PPO_predict --port 6007
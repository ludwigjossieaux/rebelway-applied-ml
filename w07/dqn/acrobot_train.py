# pip install 'stable-baselines3[extra]'
# https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

env = DummyVecEnv([lambda: gym.make("Acrobot-v1")])

# # train
# model = DQN('MlpPolicy', env, verbose=1, device="cuda")
# model.learn(total_timesteps=100000)

# # save model
# model.save('dqn_train_acrobot')

model = DQN(
    "MlpPolicy",
    env,
    verbose=1,
    device="cuda",
    learning_rate=1e-3,
    buffer_size=200_000,
    learning_starts=10_000,
    batch_size=256,
    train_freq=4,
    gradient_steps=1,
    target_update_interval=10_000,
    exploration_fraction=0.2,
    exploration_final_eps=0.05,
)
model.learn(total_timesteps=1_000_000)
model.save("dqn_train_acrobot")

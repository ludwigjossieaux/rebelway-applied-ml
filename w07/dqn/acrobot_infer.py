import os
import numpy as np
import imageio

import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

# Create env with rgb_array rendering
base_env = gym.make("Acrobot-v1", render_mode="rgb_array")
env = DummyVecEnv([lambda: base_env])

# Load trained model
model = DQN.load("dqn_train_acrobot")

video_path = "acrobot_infer.mp4"
fps = 30
max_steps = 1000
frames = []

obs = env.reset()

# Capture initial frame
frame = env.envs[0].render()
if frame is not None:
    frames.append(frame)

for _ in range(max_steps):
    action, _ = model.predict(obs, deterministic=True)
    obs, rewards, dones, infos = env.step(action)

    frame = env.envs[0].render()
    if frame is not None:
        frames.append(frame)

    if dones[0]:
        obs = env.reset()
        frame = env.envs[0].render()
        if frame is not None:
            frames.append(frame)

env.close()

# Write MP4 (avoid macroblock resizing warning by disabling it)
frames = [np.asarray(f, dtype=np.uint8) for f in frames]
imageio.mimsave(video_path, frames, fps=fps, macro_block_size=None)

print(f"Saved video to: {os.path.abspath(video_path)}")

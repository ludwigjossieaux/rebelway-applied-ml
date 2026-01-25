import os
import json
import gymnasium as gym
from gymnasium.wrappers import RecordVideo

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import BaseCallback

def train_and_save(env_id: str, timesteps: int, model_path: str, seed: int = 0):
    vec_env = make_vec_env(env_id, n_envs=8, seed=seed)

    model = PPO(
        "MlpPolicy",
        vec_env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=1024,
        batch_size=64,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        device="cuda",
        seed=seed,
    )

    model.learn(total_timesteps=timesteps)

    # save last model
    os.makedirs(os.path.dirname(model_path) or ".", exist_ok=True)
    model.save(model_path)

    # save metadata
    meta = {"env_id": env_id, "timesteps": timesteps, "seed": seed}
    with open(model_path + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    vec_env.close()
    return model


def load_model(model_path: str):
    return PPO.load(model_path, device="cuda")


def record_videos(model: PPO, env_id: str, out_dir: str, episodes: int = 5, seed: int = 123):
    os.makedirs(out_dir, exist_ok=True)

    env = gym.make(env_id, render_mode="rgb_array")
    env = RecordVideo(
        env,
        video_folder=out_dir,
        episode_trigger=lambda ep: True,  # record every episode
        name_prefix=f"{env_id}_ppo",
        disable_logger=True,
    )

    for ep in range(episodes):
        obs, info = env.reset(seed=seed + ep)
        terminated = truncated = False
        while not (terminated or truncated):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)

    env.close()
    print("Model saved to:", os.path.abspath(model_path))
    print("Videos saved to:", os.path.abspath(out_dir))


if __name__ == "__main__":
    env_id = "LunarLander-v3"
    model_path = "./models/lunarlander_ppo_last"
    video_dir = "./lunarlander_videos"
    timesteps = 1_000_000

    # Train + save last model / load model
    model = train_and_save(env_id, timesteps=timesteps, model_path=model_path, seed=0)
    # model = load_model(model_path)

    # Record videos
    record_videos(model, env_id, out_dir=video_dir, episodes=5, seed=123)

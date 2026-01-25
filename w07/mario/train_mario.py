import os
import gym_super_mario_bros
from gymnasium.wrappers import GrayscaleObservation
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
import shimmy

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack, VecVideoRecorder
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback, CallbackList


# NES wrapper compatibility patch (common workaround)
JoypadSpace.reset = lambda self, **kwargs: self.env.reset(**kwargs)


def make_mario_env(render_mode=None, seed=None):
    def _make():
        env = gym_super_mario_bros.make(
            "SuperMarioBros-v0",
            apply_api_compatibility=True,
            render_mode=render_mode,
        )

        if seed is not None:
            env.reset(seed=seed)

        # nes_py wrapper first (works best on the original env)
        env = JoypadSpace(env, SIMPLE_MOVEMENT)

        # IMPORTANT: convert Gym -> Gymnasium (fixes the Box assertion)
        env = shimmy.GymV26CompatibilityV0(env=env)

        # now Gymnasium wrappers are safe
        env = GrayscaleObservation(env, keep_dim=True)
        env = Monitor(env)
        return env

    venv = DummyVecEnv([_make])
    venv = VecFrameStack(venv, n_stack=4, channels_order="last")
    return venv


class EvalVideoCallback(BaseCallback):
    """
    Every eval_freq steps:
      - runs one deterministic evaluation episode (or up to max_steps)
      - records a video to videos/
      - logs eval episode reward to TensorBoard
    """
    def __init__(self, eval_freq, video_folder, max_steps=4500, verbose=1):
        super().__init__(verbose)
        self.eval_freq = int(eval_freq)
        self.video_folder = video_folder
        self.max_steps = int(max_steps)
        os.makedirs(self.video_folder, exist_ok=True)

    def _on_step(self) -> bool:
        if self.num_timesteps > 0 and (self.num_timesteps % self.eval_freq == 0):
            self._record_eval_video_and_log()
        return True

    def _record_eval_video_and_log(self):
        # Fresh eval env with rgb_array rendering enabled
        eval_env = make_mario_env(render_mode="rgb_array", seed=123)

        # Wrap with video recorder: record from the start of the rollout
        video_name_prefix = f"step_{self.num_timesteps}"
        eval_env = VecVideoRecorder(
            eval_env,
            video_folder=self.video_folder,
            record_video_trigger=lambda step: step == 0,
            video_length=self.max_steps,
            name_prefix=video_name_prefix,
        )

        obs = eval_env.reset()
        done = False
        ep_reward = 0.0
        steps = 0

        while not done and steps < self.max_steps:
            action, _ = self.model.predict(obs, deterministic=True)
            obs, reward, dones, infos = eval_env.step(action)

            ep_reward += float(reward[0])
            done = bool(dones[0])
            steps += 1

        # Log to TensorBoard
        self.logger.record("eval/episode_reward", ep_reward)
        self.logger.record("eval/episode_length", steps)
        self.logger.dump(self.num_timesteps)

        eval_env.close()

        if self.verbose:
            print(f"[Eval] steps={self.num_timesteps} reward={ep_reward:.1f} len={steps} video={video_name_prefix}.mp4")


def main():
    checkpoint_path = "./train"
    log_dir = "./logs"
    video_dir = "./videos"

    os.makedirs(checkpoint_path, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)

    # Training env: no render_mode for speed
    env = make_mario_env(render_mode=None, seed=0)

    model = PPO(
        "CnnPolicy",
        env,
        verbose=1,
        tensorboard_log=log_dir,
        device="cuda",
        learning_rate=2.5e-4,   # (1e-6 is usually *very* slow)
        n_steps=512,
        batch_size=256,
        n_epochs=4,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.1,
    )

    checkpoint_cb = CheckpointCallback(
        save_freq=100_000,
        save_path=checkpoint_path,
        name_prefix="ppo_mario",
        save_replay_buffer=False,
        save_vecnormalize=False,
    )

    eval_video_cb = EvalVideoCallback(
        eval_freq=25_000,     # record every 50k steps (adjust as you like)
        video_folder=video_dir,
        max_steps=4500,       # ~1 episode cap
        verbose=1,
    )

    callback = CallbackList([checkpoint_cb, eval_video_cb])

    model.learn(total_timesteps=1_000_000, callback=callback)
    model.save(os.path.join(checkpoint_path, "final_model"))

    print("done training")


if __name__ == "__main__":
    main()

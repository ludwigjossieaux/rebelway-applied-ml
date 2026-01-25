import os
import time
import numpy as np
import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

import imageio
from tqdm import trange

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env = gym.make("Acrobot-v1", render_mode="rgb_array")

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

replay_buffer = deque(maxlen=100000)

batch_size = 64
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.01
learning_rate = 0.001

input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n

dqn = DQN(input_dim, output_dim).to(device)
optimizer = optim.Adam(dqn.parameters(), lr=learning_rate)
loss_fn = nn.SmoothL1Loss()

target_dqn = DQN(input_dim, output_dim).to(device)
target_dqn.load_state_dict(dqn.state_dict())
target_dqn.eval()

target_update_every = 500  # gradient steps between target updates
grad_steps = {"n": 0}

def select_action(state, eps):
    if random.random() < eps:
        return env.action_space.sample()
    state_t = torch.tensor(state, dtype=torch.float32, device=device)
    with torch.no_grad():
        q_values = dqn(state_t)
    return torch.argmax(q_values).item()

def train_step():
    """Runs one gradient step. Returns loss float (or None if not enough data)."""
    if len(replay_buffer) <= batch_size:
        return None

    batch = random.sample(replay_buffer, batch_size)
    states, actions, rewards, next_states, dones = zip(*batch)

    states = torch.tensor(np.array(states), dtype=torch.float32, device=device)
    actions = torch.tensor(actions, dtype=torch.int64, device=device).unsqueeze(1)
    rewards = torch.tensor(rewards, dtype=torch.float32, device=device)
    next_states = torch.tensor(np.array(next_states), dtype=torch.float32, device=device)
    dones = torch.tensor(dones, dtype=torch.float32, device=device)

    current_q = dqn(states).gather(1, actions).squeeze(1)
    with torch.no_grad(): # == detach()
        next_q = target_dqn(next_states).max(dim=1).values
        target_q = rewards + gamma * next_q * (1.0 - dones)

    loss = loss_fn(current_q, target_q)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    grad_steps["n"] += 1
    if grad_steps["n"] % target_update_every == 0:
        target_dqn.load_state_dict(dqn.state_dict())

    return float(loss.item())

# -------------------
# training with progress/logs
# -------------------
episodes = 1000
max_steps_per_ep = 500

log_every = 10          # print/log every N episodes
save_every = 200        # save checkpoint every N episodes
checkpoint_path = "dqn_checkpoint.pt"

start_time = time.time()
pbar = trange(1, episodes + 1, desc="Training", unit="ep")

for episode in pbar:
    ep_start = time.time()
    state, _ = env.reset()

    total_reward = 0.0
    steps = 0
    last_loss = None

    for t in range(max_steps_per_ep):
        action = select_action(state, epsilon)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        replay_buffer.append((state, action, reward, next_state, done))
        state = next_state
        total_reward += float(reward)
        steps += 1

        # do a learning step each environment step (like your original intent)
        loss_val = train_step()
        if loss_val is not None:
            last_loss = loss_val

        if done:
            break

    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

    # update tqdm bar live
    ep_time = time.time() - ep_start
    sps = steps / max(ep_time, 1e-9)  # steps per second

    pbar.set_postfix({
        "R": f"{total_reward:.1f}",
        "steps": steps,
        "eps": f"{epsilon:.3f}",
        "loss": "n/a" if last_loss is None else f"{last_loss:.4f}",
        "buf": len(replay_buffer),
        "sps": f"{sps:.0f}",
    })

    # occasional plain logs (useful when tqdm output is buffered in SSH)
    if episode % log_every == 0 or episode == 1:
        elapsed = time.time() - start_time
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"ep={episode:4d}/{episodes} "
            f"reward={total_reward:7.2f} steps={steps:3d} "
            f"eps={epsilon:.4f} "
            f"loss={'n/a' if last_loss is None else f'{last_loss:.6f}'} "
            f"buffer={len(replay_buffer)} "
            f"elapsed={elapsed/60:.1f}m"
        )

    # checkpoint
    if episode % save_every == 0:
        torch.save({
            "episode": episode,
            "model_state_dict": dqn.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "epsilon": epsilon,
        }, checkpoint_path)
        print(f"Checkpoint saved: {os.path.abspath(checkpoint_path)}")

# -------------------
# record an episode to MP4
# -------------------
video_path = "acrobot_dqn.mp4"
fps = 30
max_steps = 500

frames = []
state, _ = env.reset()

frame = env.render()
if frame is not None:
    frames.append(frame)

for _ in range(max_steps):
    action = select_action(state, eps=0.0)
    state, reward, terminated, truncated, info = env.step(action)

    frame = env.render()
    if frame is not None:
        frames.append(frame)

    if terminated or truncated:
        break

env.close()

frames = [np.asarray(f, dtype=np.uint8) for f in frames]
imageio.mimsave(video_path, frames, fps=fps)
print(f"Saved video to: {os.path.abspath(video_path)}")

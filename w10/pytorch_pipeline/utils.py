import torch
from pathlib import Path

def save_model(model: torch.nn.Module, target_dir: str, filename: str):
    """Saves a PyTorch model to the specified path."""
    target_dir_path = Path(target_dir)
    target_dir_path.mkdir(parents=True, exist_ok=True)    
    assert filename.endswith(".pth") or filename.endswith(".pt"), "Filename should end with .pth or .pt"    
    file_path = target_dir_path / filename
    torch.save(model.state_dict(), file_path)
import torch
from tqdm import tqdm
from typing import Tuple, List, Dict

def train_step(model: torch.nn.Module, dataloader: torch.utils.data.DataLoader, loss_fn: torch.nn.Module, optimizer: torch.optim.Optimizer, device: torch.device) -> Tuple[float, float]:
    """Trains a PyTorch model for a single epoch."""
    model.train()
    train_loss, train_acc = 0.0, 0.0
    
    for batch, (X, y) in enumerate(tqdm(dataloader, desc="Training", leave=False)):
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        y_pred = model(X)
        loss = loss_fn(y_pred, y)
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item() * X.size(0)
        _, predicted = torch.max(y_pred, 1)
        train_acc += (predicted == y).sum().item()
    
    train_loss /= len(dataloader.dataset)
    train_acc /= len(dataloader.dataset)
    
    return train_loss, train_acc


def test_step(model: torch.nn.Module, dataloader: torch.utils.data.DataLoader, loss_fn: torch.nn.Module, device: torch.device) -> Tuple[float, float]:
    """Tests a PyTorch model for a single epoch."""
    model.eval()
    test_loss, test_acc = 0.0, 0.0
    
    with torch.inference_mode():    
        for batch, (X, y) in enumerate(tqdm(dataloader, desc="Testing", leave=False)):
            X, y = X.to(device), y.to(device)
            y_pred = model(X)
            loss = loss_fn(y_pred, y)            
            test_loss += loss.item()
            
            test_pred_labels = torch.argmax(y_pred, 1)
            test_acc += (test_pred_labels == y).sum().item() / len(test_pred_labels)
    
    test_loss /= len(dataloader.dataset)
    test_acc /= len(dataloader.dataset)
    
    return test_loss, test_acc

def train(model: torch.nn.Module, train_dataloader: torch.utils.data.DataLoader, test_dataloader: torch.utils.data.DataLoader, optimizer: torch.optim.Optimizer, loss_fn: torch.nn.Module, device: torch.device, epochs: int) -> Tuple[List[float], List[float], List[float], List[float]]:
    """Trains and tests a PyTorch model for a number of epochs."""
    results = {
        "train_loss": [],
        "train_acc": [],
        "test_loss": [],
        "test_acc": []
    }
    for epoch in tqdm(range(epochs), desc="Epochs"):
        train_loss, train_acc = train_step(model, train_dataloader, loss_fn, optimizer, device)
        test_loss, test_acc = test_step(model, test_dataloader, loss_fn, device)
        
        results["train_loss"].append(train_loss)
        results["train_acc"].append(train_acc)
        results["test_loss"].append(test_loss)
        results["test_acc"].append(test_acc)
        
        print(f"Epoch: {epoch+1} | Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.4f}")
    
    return results["train_loss"], results["train_acc"], results["test_loss"], results["test_acc"]
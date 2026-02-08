import os
import torch
import data_setup, engine, TINYVGG, utils
from torchvision import transforms

NUM_EPOCHS = 5
BATCH_SIZE = 32
HIDDEN_UNITS = 50
LEARNING_RATE = 0.001

train_dir = "./data/GuavaDiseaseDataset/train"
test_dir = "./data/GuavaDiseaseDataset/test"

if __name__ == "__main__":
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    data_transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])
    
    train_dataloader, test_dataloader, class_names = data_setup.create_dataloaders(train_dir, test_dir, data_transform, BATCH_SIZE)
    model = TINYVGG.TinyVGG(input_shape=3, hidden_units=HIDDEN_UNITS, output_shape=len(class_names)).to(device)
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    engine.train(model, train_dataloader, test_dataloader, optimizer, loss_fn, device, NUM_EPOCHS)
    utils.save_model(model, target_dir="models", filename="modular_test01.pth")
    
    print("Done processing!")
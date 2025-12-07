
import os
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )
        
    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
    
class ClassifierUtils:
    
    def __init__(self):
        pass
    
    def test(self):
        return "Test from ClassifierUtils"
    
    def predict(self, image_path):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = Net().to(device)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "mnist_fashion_base_model.pth")        
        model.load_state_dict(torch.load(model_path))
        model.eval()
      
        image = Image.open(image_path).convert("L") # convert to grayscale
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((28, 28)),
        ])
        image = transform(image).to(device) # add batch dimension

        with torch.inference_mode():
            output = model(image.unsqueeze(0)) # add batch dimension
            predicted_label = output.argmax(1).item()
            return predicted_label
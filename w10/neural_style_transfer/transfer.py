import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def load_image(image_path, size=None):
    image = Image.open(image_path).convert('RGB')

    if size is not None:
        # keep aspect ratio: resize so the longest side == size
        w, h = image.size
        if w >= h:
            new_w = size
            new_h = int(h * size / w)
        else:
            new_h = size
            new_w = int(w * size / h)

        image = image.resize((new_w, new_h), Image.LANCZOS)

    transform = transforms.ToTensor()
    image = transform(image).unsqueeze(0).to(device)
    return image

class ContentLoss(nn.Module):
    def __init__(self, target):
        super(ContentLoss, self).__init__()
        self.target = target.detach()

    def forward(self, input):
        self.loss = nn.functional.mse_loss(input, self.target)
        return input
    
def gram_matrix(input):
    batch_size, feature_maps, height, width = input.size()
    features = input.view(batch_size * feature_maps, height * width)
    G = torch.mm(features, features.t())
    return G.div(batch_size * feature_maps * height * width)

class StyleLoss(nn.Module):
    def __init__(self, target):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target).detach()

    def forward(self, input):
        G = gram_matrix(input)
        self.loss = nn.functional.mse_loss(G, self.target)
        return input
    
class Normalization(nn.Module):
    def __init__(self, mean, std):
        super().__init__()
        # reshape to [1, C, 1, 1] so it broadcasts over N,H,W
        self.mean = mean.clone().detach().view(1, -1, 1, 1)
        self.std = std.clone().detach().view(1, -1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std
    
def get_style_model_and_losses(style_img, content_img):    
    cnn = models.vgg19(pretrained=True).features.to(device).eval()
    
    normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
    normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
    normalization = Normalization(normalization_mean, normalization_std).to(device)
    
    content_layers = ['conv_4']
    style_layers = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']
    
    content_losses = []
    style_losses = []
    model = nn.Sequential(normalization).to(device)

    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = f'conv_{i}'
        elif isinstance(layer, nn.ReLU):
            name = f'relu_{i}'
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = f'pool_{i}'
        elif isinstance(layer, nn.BatchNorm2d):
            name = f'bn_{i}'
        else:
            continue

        model.add_module(name, layer)

        if name in content_layers:
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module(f"content_loss_{i}", content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module(f"style_loss_{i}", style_loss)
            style_losses.append(style_loss)


    # iterate through the model in reverse order to find the last content and style loss layers, and trim the model after that
    for i in range(len(model)-1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break
        
    model = model[:(i+1)]    
        
    return model, content_losses, style_losses


def run_style_transfer(content_img, style_img, input_img, num_steps=300, style_weight=1e6, content_weight=1):
    model, content_losses, style_losses = get_style_model_and_losses(style_img, content_img)
    optimizer = optim.LBFGS([input_img.requires_grad_()])
    
    run = [0]
    while run[0] <= num_steps:
        def closure():
            with torch.no_grad():            
                input_img.data.clamp_(0, 1)
            
            optimizer.zero_grad()
            model(input_img)
            
            style_score = 0
            content_score = 0
            
            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss
            
            style_score *= style_weight
            content_score *= content_weight
            
            loss = style_score + content_score
            loss.backward()
            
            run[0] += 1
            if run[0] % 50 == 0:
                print(f"Run {run[0]}: Style Loss: {style_score.item():.4f} Content Loss: {content_score.item():.4f}")
            
            return loss
        
        optimizer.step(closure)
    
    with torch.no_grad():
        input_img.data.clamp_(0, 1)
    
    return input_img

def neural_style_transfer(content_image_path, style_image_path, output_image_path, num_steps=300, init="content"):
    content_img = load_image(content_image_path)
    content_h, content_w = content_img.size(2), content_img.size(3)
    target_size = max(content_h, content_w)
    style_img = load_image(style_image_path, size=target_size)
    
    if init == "noise":
        input_img = torch.randn_like(content_img).to(device)
    else:
        input_img = content_img.clone()
    
    output = run_style_transfer(content_img, style_img, input_img, num_steps)
    
    output_image = output.cpu().squeeze(0)
    output_image = transforms.ToPILImage()(output_image)
    output_image.save(output_image_path)
    print(f"Output image saved to {output_image_path}")
    

if __name__ == "__main__":
    content_image_path = "hills.jpg"
    style_image_path = "vangogh.jpg"
    output_image_path = "output.jpg"    
    neural_style_transfer(content_image_path, style_image_path, output_image_path, init="content")
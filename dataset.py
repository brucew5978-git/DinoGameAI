from torch.utils.data import Dataset
import os
from PIL import Image
from torchvision import transforms
from torch.utils.data import DataLoader

class CustomImageDataset(Dataset):
    def __init__(self, root_dir, labels, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_list = os.listdir(root_dir)

        self.labels = labels

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        img_path = os.path.join(self.root_dir, self.image_list[idx])
        image = Image.open(img_path)

        if self.transform:
            image = self.transform(image)

        label = self.labels[idx]
        return image, label


transforms_list = [
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
]
transform =transforms.Compose(transforms_list)

labels = ["0", "1"]
imagePath = "data"
dataset = CustomImageDataset(imagePath, labels=labels, transform=transform)

data_loader = DataLoader(dataset, batch_size=32, shuffle=True)
print(data_loader)

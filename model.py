import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
from PIL import Image
import os

class CustomDataset(Dataset):
    def __init__(self, root_dir, labels, transform=None):
        self.root_dir = root_dir
        self.labels = labels
        self.transform = transform
        self.img_paths = [os.path.join(root_dir, f) for f in os.listdir(root_dir)]

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img = Image.open(self.img_paths[idx])
        img = img.resize((887, 341))
        if self.transform:
            img = self.transform(img)
        label = self.labels[idx]
        return img, label

# Define the CNN architecture
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        
        self.fc3 = nn.Linear(84, 2)
        #Last layer of the net outputs 2 classes

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x



# Initialize the CNN
net = Net()

# Define a loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# Define the transforms for the training data
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

#Creating list of labels for training data
TRAINING_JUMP_IMG_COUNT = 28
TRAINING_NORMAL_IMG_COUNT = 110
imgLabel = []

for i1 in range(TRAINING_JUMP_IMG_COUNT):
    imgLabel.append(1)

for i2 in range(TRAINING_NORMAL_IMG_COUNT):
    imgLabel.append(0)


# Load the custom dataset
root = os.getcwd() + "/data/train"
trainset = CustomDataset(root_dir=root, labels=imgLabel, transform=transform)
trainloader = DataLoader(trainset, batch_size=100, shuffle=True, num_workers=0)



# Train the network
for epoch in range(100):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        #Converting labels to a LongTensor
        labels = torch.LongTensor(labels)    

        # clear parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
    print('Epoch %d loss: %.3f' % (epoch + 1, running_loss / (i+1)))
    ''''''

print('Finished Training')

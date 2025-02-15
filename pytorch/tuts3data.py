# Datasets & DataLoaders

# https://pytorch.org/tutorials/beginner/basics/data_tutorial.html


# Loading a Dataset
# Loading the Fashion-MNIST dataset.
# https://research.zalando.com/project/fashion_mnist/fashion_mnist/

# root is the path where the train/test data is stored.
# train specifies training or test dataset.
# download=True downloads the data from the Internet if it's not available at root.
# transform and target_transform specify the feature and label transformations.



import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor()
)

test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor()
)


# Iterating and Visualizing the Dataset
# We can index Datasets manually like a list:
# training_data[index]
# We use matplotlib to visualize some samples in our training data.

labels_map = {
    0: "T-Shirt",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Shoe",
    6: "Shirt",
    7: "Sandal",
    8: "Shirt",
    9: "Sneaker",
    10: "Bag",
    11: "Ankle Boot",
    12: "Sandal",
    13: "Jacket"
}


figure = plt.figure(figsize=(8, 8))
cols, rows = 3, 3
for i in range(1, cols * rows + 1):
    sample_idx = torch.randint(len(training_data), size=(1,)).item()
    img, label = training_data[sample_idx]
    figure.add_subplot(rows, cols, i)
    plt.title(labels_map[label])
    plt.axis("off")
    plt.imshow(img.squeeze(), cmap="gray")
plt.show()


# Creating a Custom Dataset for your files.
# A custom Dataset class must implement three functions:
# __init__
# __len__
# __getitem__
# Take a look at this implementation; the FashionMNIST images
# are stored in a directory img_dir, and their labels are stored
# separately in a CSV file annotations_file.

import os
import pandas as pd
from torchvision.io import read_image

class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)
    
    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
    

def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
    self.img_labels = pd.read_csv(annotations_file)
    self.img_dir = img_dir
    self.transform = transform
    self.target_transform = target_transform


def __len__(self):
    return len(self.img_labels)


def __getitem__(self, idx):
    img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
    image = read_image(img_path)
    label = self.img_labels.iloc[idx, 1]
    if self.transform:
        image = self.transform(image)
    if self.target_transform:
        label = self.target_transform(label)
    return image, label


# The __init__ fucntion is run once while instantiating the Dataset object.
# Initialize the directory containing images, annotations file, and both transforms.

def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
    self.img_labels = pd.read_csv(annotations_file)
    self.img_dir = img_dir
    self.transform = transform
    self.target_transform = target_transform



# The __len__ function returns the number of samples in our dataset.

def __len__(self):
    return len(self.img_labels)


# The __getitem__ function loads and returns a sample from the dataset at the given index, idx.
# The __getitem__ function identifies the image's location on disk, converts that to a tensor using:
# read corresponding label from the csv data in self.img_labels.
# The __getitem__ function calls the transform functions on them and returns the
# tensor image and corresponding label in a tuple.

def __getitem__(self, idx):
    img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx,0])
    image = read_image(img_path)
    label = self.img_labels.iloc[idx, 1]
    if self.transform:
        image = self.transform(image)
    if self.target_transform:
        label = self.target_transform(label)
    return image, label


# Preparing your data for training with DataLoaders.
# The Dataset retrieves our dataset's features and labels pass samples in minibatches,
# reshuffle the data at every speed up data retrieval.

from torch.utils.data import DataLoader

train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=64, shuffle=True)


# Iterate through the DataLoader.
# We have loaded that dataset into the DataLoader and can iterate through the dataset as needed.
# Each iteration below returns a batch of train_features and train_labels (each with batch_size=64).
# After we iterate over all batches the data is shuffled (for finer-grained control over the data loading order).

# Display image and label.

train_features, train_labels = next(iter(train_dataloader))
print(f"Feature batch shape: {train_features.size()}")
print(f"Labels batch shape: {train_labels.size()}")
img = train_features[0].squeeze()
label = train_labels[0]
plt.imshow(img, cmap="gray")
plt.show()
print(f"Label: {label}")
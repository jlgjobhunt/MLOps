# Transforms
# https://pytorch.org/tutorials/beginner/basics/transforms_tutorial.html
# We use transforms to perform some manipulation of the data and make it suitable for training.
# All TorchVision datasets have two parameters that accept callables
# containing the transformation logic.
# The torchvision.transforms module offers several commonly-used transforms out of the box.
# -transform   (modifies features)
# -target_transform (modify the labels)


import torch
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda


ds = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
    target_transform=Lambda(lambda y: torch.zeros(10, dtype=torch.float).scatter_(0, torch.tensor(y), value=1))
)


# ToTensor converts a PIL image or NumPy ndarray into a FloatTensor
# and scales the image's pixel intensity valeu in the range [0., 1.]


# Lambda Transforms
# Lambda transforms apply any user-defined lambda function.
# Here, we define a function to turn the integer into a one-hot encoded tensor.
# It first creates a zero tensor of size 10 (for labels in the dataset)
# and calls which assigns a value=1 on the index as given by the label 'y'.

target_transform = Lambda(lambda y: torch.zeros(10, dtype=torch.float).scatter_(dim=0, index=torch.tensor(y), value=1))


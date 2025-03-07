# Warmstarting model using parameters from a different PyTorch Model

# Partially loading a model or loading a partial model are common scenarios
# when transfer learning or training a new complex model.
# Leveraging trained parameters, even if only a few are usable, will help to warmstart
# the training process and hopefully help your model converge much faster
# than training from scratch.
# https://pytorch.org/tutorials/recipes/recipes/
# warmstarting_model_using_parameters_from_a_different_model.htmlz



# Whether you are loading from a partial state_dict, which is missing some keys, or loading
# a state_dict with more keys than the model that you are loading into, you can set the strict
# argument to False in the load_state_dict() function to ignore non-matching keys.
# In this recipe, we will experiment with warmstarting a model using parameters
# of a different model.
#   1. Import all necessary libraries for loading our data.
#   2. Define and initialize the neural network A and B.
#   3. Save model A.
#   4. Load into model B.


# 1. Import necessary libraries for loading our data.
#    For this recipe, we will use torch and its subsidiaries torch.nn and torch.optim.


import torch
import torch.nn as nn
import torch.optim as optim



# 2. Define and initialize the neural network A and B.
# We will create a neural network for training images.
# To learn more see the Defining a Neural Network recipe.
# We will create two neural networks for sake of loading one parameter of type A into type B.

class NetA(nn.Module):
    def __init__(self):
        super(NetA, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(nn.relu(self.conv1(x)))
        x = self.pool(nn.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = nn.relu(self.fc1(x))
        x = nn.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
netA = NetA()


class NetB(nn.Module):
    def __init__(self):
        super(NetB, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(nn.relu(self.conv1(x)))
        x = self.pool(nn.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = nn.relu(self.fc1(x))
        x = nn.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
netB = NetB()


import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


# Download training data from open datasets.

training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)


# Download test data from open datasets.

test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)


# Create data loaders with a batch size of 64 features and labels per element.
batch_size = 64

train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader =  DataLoader(test_data, batch_size=batch_size)

for X, y in test_dataloader:
    print(f"Shape of X [N, C, H, W]: {X.shape}")
    print(f"Shape of y: {y.shape} {y.dtype}")
    break


device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"

print(f"Using {device} device.")


# Define model.

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
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
    
model = NeuralNetwork().to(device)
print(model)


# Call the model on the input returns a 2-dimensional tensor with dim=0 corresponding to each
# output of 10 raw predicted values for each class, and dim=1 corresponding to individual values
# of each output. We get the prediction probabilities by passing it through an instance
# of the nn.Softmax module.


X = torch.rand(1, 28, 28, device=device)
logits = model(X)
pred_probab = nn.Softmax(dim=1)(logits)
y_pred = pred_probab.argmax(1)
print(f"Predicted class: {y_pred}")



# Model Layers
# Take a sample minibatch fo 3 images of size 28 x 28 pass through the neural network.

input_image = torch.rand(3, 28, 28)
print(input_image.size())



# Initialize the nn.Flatten layer to convert each 2D 28 x 28 image
# into contiguous array of 784 pixel values (the minibatch dimension (at dim=0) is maintained).

flatten = nn.Flatten()
flat_image = flatten(input_image)
print(flat_image.size())



# The linear layer, nn.Linear, is a module that applies a linear transformation on the input using its stored weights and biases.

layer1 = nn.Linear(in_features=28*28, out_features=20)
hidden1 = layer1(flat_image)
print(hidden1.size())


# The non-linear activations are what create the complex mappings between the model's inputs and outputs.
# They are applied after linear transformations to introduce nonlinearity, helping neural networks learn
# a wide variety of phenomena. In this model, we use nn.ReLU between our linear layers, but there's other
# activations to introduce non-linearity in your model.

print(f"Before ReLU: {hidden1}\n\n")
hidden1 = nn.ReLU()(hidden1)
print(f"After ReLU: {hidden1}")


# The ordered container of modules is layer, nn.Sequential, is an ordered container of modules.
# The data is passed through all the modules in the same order as defined.
# You can use sequential containers to put together a quick network like seq_modules.

seq_modules = nn.Sequential(
    flatten,
    layer1,
    nn.ReLU(),
    nn.Linear(20, 10)
)
input_image = torch.rand(3,28,28)
logits = seq_modules(input_image)


# The last linear layer of the neural network returns logits - raw valeus in [-infty, infty]
# which are passed to the nn.Softmax module. The logits are scaled to values [0, 1] representing
# the model's predicted probabilities for each class. 
# The dim parameter indicates the dimension along which the values must sum to 1.

softmax = nn.Softmax(dim=1)
pred_probab = softmax(logits)



# Many layers inside a neural network are parameterized, i.e. have associated weights and biases
# that are optimized during training. Subclassing nn.Module automatically tracks all fields defined
# inside your model object, and makes all parameters accessible using your model's parameters()
# or named_parameters() methods. Iterate over each parameter and print the size and preview of its vlaues.

print(f"Model structure: {model}\n\n")

for name, param in model.named_parameters():
    print(f"Layer: {name} | Size: {param.size()} | Values: {param[:2]} \n")


# Optimizing the Model Parameters
# Use a loss function and an optimizer.

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)


# In a single training loop, the model makes predictions on training dataset,
# and backpropagates the prediction error to adjust the model's parameters.

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error.
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation.
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")


# We also check the model's performance against the test dataset to ensure it is learning.

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


# The training process is conducted over several iterations (epochs).
# Each epoch's revisions to the model means learning new parameters to make
# better predictions. The model's accuracy and loss at each epoch, we'd like to see
# the accuracy increase and the loss decrease with every epoch.

epochs = 5
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)
print("Done!")



# Saving Models
# A common way to save a model is to serialize the internal state dictionary
# (containing the model parameters).

torch.save(model.state_dict(), "model.pth")
print("Saved PyTorch Model State to model.pth")



# Loading Models
# The process for loading a model includes re-creating the model structure
# and loading the state dictionary into it.

model = NeuralNetwork().to(device)
model.load_state_dict(torch.load("model.pth", weights_only=True))


# This model can now be used to make predictions.

classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

model.eval()
x, y = test_data[0][0], test_data[0][1]
with torch.no_grad():
    x = x.to(device)
    pred = model(x)
    predicted, actual = classes[pred[0].argmax(0)], classes[y]
    print(f"Predicted: '{predicted}', Actual: '{actual}' ")
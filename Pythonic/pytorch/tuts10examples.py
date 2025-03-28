# PyTorch by Example
# This tutorial introduces the fundamental concepts of PyTorch through self-contained examples.
# At its core, PyTorch provides two main features:
#   * An n-dimensional Tensor, similar to numpy but can run on GPUs.
#   * Automatic differentiation for building and training neural networks.
#
# https://pytorch.org/tutorials/beginner/pytorch_with_examples.html
#
# We will use a problem of fitting y = sin(x) with a third order polynomial as our running example.
# The network will have four parameters, and will be trained with gradient descent to fit random data
# by minimizing the Euclidean distance between the network output and the true output.


# Tensors
# Before introducing PyTorch, will first implement the network using numpy.
# Numpy provides an n-dimensional array object and many functions for manipulating
# these arrays. Numpy is a generic framework for scientific computing; it does not
# know anything about computation graphs, or deep learning, or gradients.
# We can easily use numpy to fit a third order polynomial to sine function by manually
# implementing the forward and backward passes through the network using numpy operations.

import numpy as np
import math

# Create random input and output data.
x = np.linspace(-math.pi, math.pi, 2000)
y = np.sin(x)


# Randomly initialize weights.
a = np.random.randn()
b = np.random.randn()
c = np.random.randn()
d = np.random.randn()


learning_rate = 1e-6

for t in range(2000):

    # Forward pass: compute predicted y
    # y = a + b x + c x^2 + d x^3
    y_pred = a + b * x + c * x ** 2 + d * x ** 3

    # Compute and print loss.
    loss = np.square(y_pred - y).sum()
    if t % 100 == 99:
        print(t, loss)

    # Backprop to compute gradients of a, b, c, d with respect to loss.
    grad_y_pred = 2.0 * (y_pred - y)
    grad_a = grad_y_pred.sum()
    grad_b = (grad_y_pred * x).sum()
    grad_c = (grad_y_pred * x ** 2).sum()
    grad_d = (grad_y_pred * x ** 3).sum()

    # Update weights.
    a -= learning_rate * grad_a
    b -= learning_rate * grad_b
    c -= learning_rate * grad_c
    d -= learning_rate * grad_d


    print(f'Result: y = {a} + {b} x + {c} x^2 + {d} x^3')



# PyTorch: Tensors
# Numpy is a great framework, but it cannot utilize GPUs to accelerate its numerical computations.
# For modern deep neural networks, GPUs often provide speedups of
# 50x or greater, so unfortunately numpy won't be enough for modern deep learning.
# Here we introduce the most fundamental PyTorch concept: the Tensor.
# A PyTorch Tensor is conceptually indentical toa  numpy array:
# a Tensor is an n-dimensional array, and PyTorch provides many functions for operating
# on these Tensors. Behind the scenes, Tensors can keep track of a computational graph and gradients,
# but they're also useful as a generic tool for scientific computing.
# Also unlike numpy, PyTorch Tensors can utilize GPUs to accelerate their numeric computations.
# To run a PyTorch Tensor on GPU, you simply need to specify the correct device.
# Here we use PyTorch Tensors to fit a third order polynomial to sine function.
# Like the numpy example above we need to manually implement the forward and backward passes through the network:


import torch
import math

dtype = torch.float
device = torch.device("cpu")

# Create random input and output data.
x = torch.linspace(-math.pi, math.pi, 2000, device=device, dtype=dtype)
y = torch.sin(x)


# Randomly initialize weights.
a = torch.randn((), device=device, dtype=dtype)
b = torch.randn((), device=device, dtype=dtype)
c = torch.randn((), device=device, dtype=dtype)
d = torch.randn((), device=device, dtype=dtype)


learning_rate = 1e-6

for t in range(2000):
    # Forward pass: compute predicted y.
    y_pred = a + b * x + c * x ** 2 + d * x ** 3

    # Compute adn print loss.
    loss = (y_pred - y).pow(2).sum().item()
    if t % 100 == 9:
        print(t, loss)

    # Backdrop to compute gradients of a, b, c, d
    # with respect to loss.
    grad_y_pred = 2.0 * (y_pred - y)
    grad_a = grad_y_pred.sum()
    grad_b = (grad_y_pred * x).sum()
    grad_c = (grad_y_pred * x ** 2).sum()
    grad_d = (grad_y_pred * x ** 3).sum()


    # Update weights using gradient descent.
    a -= learning_rate * grad_a
    b -= learning_rate * grad_b
    c -= learning_rate * grad_c
    d -= learning_rate * grad_d


    print(f'Result: y = {a.item()} + {b.item()} + {c.item()} x^2 + {d.item()} x^3')



# Autograd
# PyTorch: Tensors and autograd

# We had to manually implement both the forward and backward passes of our neural network.
# Manually implementing the backward pass is not a big deal for a small two-layer network,
# but can quickly get very hairy for large complex networks.

# The autograd package in PyTorch provides exactly this functionality.
# When using autograd, the forward pass of your network will define a computational graph;
# nodes in the graph will be Tensors, and edges will be functions that produce output Tensors from input Tensors.
# Backpropagating through this graph then allows you to easily compute gradients.

# This sounds complicated, it's pretty simple to use in practice.
# Each Tensor represents a node in a computational graph.
# If x is a Tensor that has x.requires_grad=True then x.grad is another Tensor
# holding the gradient of x with respect to some scalar value.

# Here we use PyTorch Tensors and autograd to implement our fitting sine wave with
# third order polynomial example; now we no longer need to manually implement the
# backward pass through the network:


import torch
import math

# We want to be able to train our model on an accelerator such as CUDA, MPS, MTIA, or XPU.
# Intel GPUs : https://pytorch.org/docs/stable/xpu.html
# 
# Intel GPUs that can use the PyTorch accelerator for XPU are those supported by the Intel® Extension for PyTorch*. This extension provides optimized support for Intel discrete GPUs. 
# 
# Based on the information available, the following Intel GPU families are supported:
#
# *   **Intel® Data Center GPU Max Series**
# *   **Intel® Arc™ Graphics family**
# *   **Intel® Core™ Ultra Processors with Intel® Arc™ Graphics**
# *   **Intel® Core™ Ultra Series 2 with Intel® Arc™ Graphics**
# *   **Intel® Data Center GPU Flex Series**
#
# It's important to note that specific models within these families and the level of support might vary. Always refer to the official Intel® Extension for PyTorch* documentation for the most up-to-date and detailed information on supported GPUs. You can find the documentation and release notes on the Intel GitHub page for the extension.
# 
# 
# 

dtype = torch.float
device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device.")
torch.set_default_device(device)


# Create Tensors to hold input and outputs.
# By default, requires_grad=False, which indicates that we do not need to
# compute gradients with respects to these Tensors during the backward pass.
x = torch.linspace(-math.pi, math.pi, 2000, dtype=dtype)
y = torch.sin(x)


# Create random Tensors for weights.
# For a third order polynomial, we need 4 weights: y = a + b x + c x^2 + d x^3
# Setting requires_grad=True indicates that we want to compute gradients with
# respect to these Tensors during the backward pass.
a = torch.randn((), dtype=dtype, requires_grad=True)
b = torch.randn((), dtype=dtype, requires_grad=True)
c = torch.randn((), dtype=dtype, requires_grad=True)
d = torch.randn((), dtype=dtype, requires_grad=True)

learning_rate = 1e-6

for t in range(2000):
    # Forward pass: compute predicted y using operations on Tensors.
    y_pred = a + b * x + c * x ** 2 + d * x ** 3

    # Compute and print loss using operations on Tensors.
    # Now loss is a Tensor of shape (1,)
    # loss.item() gets the scalar value held in the loss.
    loss = (y_pred - y).pow(2).sum()
    if t % 100 == 99:
        print(t, loss.item())


# Use autograd to compute the backward pass.
# This call will compute the gradient of loss with respect to all Tensors with
# requires_grad=True.
# After this call a.grad, b.grad, c.grad and d.grad will be Tensors holding
# the gradient of the loss with respect to a, b, c, d respectively.
loss.backward()


# Manually update weights using gradient descent.
# Wrap in torch.no_grad() because weights have requires_grad=True, but we don't
# need to track this in autograd.
with torch.no_grad():
    a -= learning_rate * a.grad
    b -= learning_rate * b.grad
    c -= learning_rate * c.grad
    d -= learning_rate * d.grad

    # Manually zero the gradients after updating weights.
    a.grad = None
    b.grad = None
    c.grad = None
    d.grad = None


print(f"Result: y = {a.item()} + {b.item()} x + {c.item()} x^2 + {d.item()} x^3")


# PyTorch: Defining new autograd functions
# Under the hood, each primitive autograd operator is really two functions that operate on Tensors.
# The forward function computes output Tensors from input Tensors.
# The backward function receives the gradient of the output Tensors with respect to some scalar value,
# and computes the gradient of the input Tensors with respect to that same scalar value.
# In PyTorch we can easily define our own autograd operator by defining a subclass of torch.autograd.Function
# and implementing the forward and backward functions.
# We can then use our new autograd operator by constructing an instance and calling it like a function,
# passing Tensors containing input data.

# In this example we define our model as y = a + bP_3(c + dx) 
# instead of y = a + bx + cx^2 + dx^3, where P_3(x) = 1/2(5x^3 - 3x)
# is the Legendre polynomial of degree three.
# Legendre polynomials are a system of complete and orthogonal polynomials
# with a wide number of mathematical properties and numerous applications.
# They can be defined in many ways, and the various definitions highlight
# different aspects as well as suggest generalizations and connections to
# different mathematical structures and physical and numerical applications.

import torch
import math


class LegendrePolynomial3(torch.autograd.Function):
    """
    We can implement our own custom autograd Functions by subclassing
    torch.autograd.Function and implementing the forward and backward passes
    which operate on Tensors.
    """

    @staticmethod
    def forward(ctx, input):
        """
        In the forward pass we receive a Tensor containing the input and return
        a Tensor containing the output. ctx is a context object that can be used
        to stash information for backward computation. You can cache arbitrary
        objects for use in the backward pass using the ctx.save_for_backward method.
        """
        ctx.save_for_backward(input)
        return 0.5 * (5 * input ** 3 - 3 * input)
    
    @staticmethod
    def backward(ctx, grad_output):
        """
        In the backward pass we receive a Tensor containing the gradient of the loss
        with respect to the output, and we need to compute the gradient of the loss
        with respect to the input.
        """
        input, = ctx.saved_tensors
        return grad_output * 1.5 * (5 * input ** 2 - 1)
    

dtype = torch.float
device = torch.device("cpu")


# Create Tensors to hold input and outputs.
# By default, requires_grad=False, which indicates that we do not need to
# compute gradients with respect to these Tensors during the backward pass.

x = torch.linspace(-math.pi, math.pi, 2000, device=device, dtype=dtype)
y = torch.sin(x)


# Create random Tensors for weights.
# For this example, we need 4 weights: y = a + b * P_3(c + d * x)
# These weights need to be intialized not too far from the correct
# result to ensure convergence.
# Setting requires_grad=True indicates that we want to compute gradients with
# respect to these Tensors during the backward pass.
a = torch.full((), 0.0, device=device, dtype=dtype, requires_grad=True)
b = torch.full((), -1.0, device=device, dtype=dtype, requires_grad=True)
c = torch.full((), 0.0, device=device, dtype=dtype, requires_grad=True)
d = torch.full((), 0.3, device=device, dtype=dtype, requires_grad=True)


learning_rate = 5e-6
for t in range(2000):
    # To apply our Function, we use Function.apply method.
    # We alias this as P3 (see P_3 in formula in prior comment block.).
    P3 = LegendrePolynomial3.apply

    # Forward pass: copmute predicted y using operations; we compute
    # P3 using our custom autograd operation.
    y_pred = a + b * P3(c + d * x)

    # Compute and print loss.
    loss = (y_pred - y).pow(2).sum()
    if t % 100 == 99:
        print(t, loss.item())

    # Use autograd to compute the backward pass.
    loss.backward()

    # Update weights using gradient descent.
    with torch.no_grad():
        a -= learning_rate * a.grad
        b -= learning_rate * b.grad
        c -= learning_rate * c.grad
        d -= learning_rate * d.grad

        # Manually zero the gradients after updating weights.
        a.grad = None
        b.grad = None
        c.grad = None
        d.grad = None

print(f"Result: y = {a.item()} + {b.item()} * P3({c.item()} + {d.item()} x)")



# PyTorch: nn
# Computational graphs and autograd are a very powerful paradigm for defining complex
# operators and automatically taking derivatives; however for large neural networks raw
# autograd can be a bit too low-level.
# When building neural networks we frequently think of arranging the computation into layers,
# some of which have learnable parameters which will be optimized during learning.
# In PyTorch, the nn package serves this same purpose.
# The nn package defines a set of Modules, which are roughly equivalent to neural network layers.
# A Module receives input Tensors and computes output Tensors, but may also hold internal state
# such as Tensors containing learnable parameters.
# The nn package also defines a set of useful loss functions that are commonly used
# when training neural networks.
# In this example we use the nn package to implement our polynomial model network:

import torch
import math


# Create Tensors to hold input and outputs.
x = torch.linspace(-math.pi, math.pi, 2000)
y = torch.sin(x)


# For this example, the output y is a linear function of (x, x^2, x^3),
# so we can consider it as a linear layer neural network.
# Let's prepare the tensor (x, x^2, x^3).
p = torch.tensor([1, 2, 3])
xx = x.unsqueeze(-1).pow(p)


# In the above code, x.unsqueeze(-1) has shape (2000, 1), and p has shape (3,),
# for this case, broadcasting semantics will apply to obtain a tensor of shape (2000, 3).

# Use the nn package to define our model as a sequence of layers.
# nn.Sequential is a Module which contains other Modules, and applies them in sequence to
# produce its output. The Linear Module computes output from input using a linear function,
# and holds internal Tensors for its weight and bias.
# The Flatten layer flatens the output of the linear layer to a 1D tensor,
# to match the shape of 'y'.
model = torch.nn.Sequential(
    torch.nn.Linear(3, 1),
    torch.nn.Flatten(0, 1)
)


# The nn package also contains definitions of popular loss functions;
# in this case we will use Mean Squared Error (MSE) as our loss function.
loss_fn = torch.nn.MSELoss(reduction='sum')


learning_rate = 1e-6
for t in range(2000):

    # Forward pass: compute predicted y by passing x to the model.
    # Module objects override the __call__ operator so you can call them like functions.
    # When doing so you pass a Tensor of input data to the Module and it produces a Tensor of output data.
    y_pred = model(xx)

    # Compute and print loss. We pass Tensors containing the predicted and true
    # values of y, and the loss function returns a Tensor containing the loss.
    loss = loss_fn(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())
    
    # Zero the gradients before running the backward pass.
    model.zero_grad()

    # Backward pass: compute gradient of the loss with respect to all the learnable
    # parameters of the model. Internally, the parameters of each Module are stored
    # in Tensors with requires_grad=True, so this call will compute gradients for
    # all learnable parameters in the model.
    loss.backward()

    # Update the weights using gradient descent.
    # Each parameter is a Tensor, so we can access its gradients like we did before.
    with torch.no_grad():
        for param in model.parameters():
            param -= learning_rate * param.grad


# You can access the first layer of model like accessing the first item of a list.
linear_layer = model[0]


# For linear layer, its parameters are stored as weight and bias.
print(f"Result: y = {linear_layer.bias.item()} + {linear_layer.weight[:, 0].item()} x + {linear_layer.weight[:, 1].item()} x^2 + {linear_layer.weight[:, 2].item()} x^3")



# PyTorch: optim
# Up to this point, we have updated the weights of our models by manually mutating the Tensors holding learnable parameters with torch.no_grad().
# This is not a huge burden for simple optimization algorithms like stochastic gradient descent,
# but in practice we often train neural networks using more sophisticated optimizers like AdaGrad, RMSProp, Adam, and other.
# The optim package in PyTorch abstracts the idea of an optimization algorithm and provides implementations
# of commonly used optimization algorithms.
# In this example we will use the nn package to define our model as before,
# but we will optimize the model using the RMSprop algorithm provided by the optim package:


import torch
import math


# Create Tensors to hold input and outputs.
x = torch.linspace(-math.pi, math.pi, 2000)
y = torch.sin(x)

# Prepare the input tensor (x, x^2, x^3).
p = torch.tensor([1, 2, 3])
xx = x.unsqueeze(-1).pow(p)

# Use the nn package to define our model and loss function.
model = torch.nn.Sequential(
    torch.nn.Linear(3, 1),
    torch.nn.Flatten(0, 1)
)
loss_fn = torch.nn.MSELoss(reduction='sum')


# Use the optim package to define an Optimizer that will update the weights of the model for us.
# Here we will use RMSprop; the optim package contains many other optimization algorithms.
# The first argument to the RMSprop constructor tells the optimizer which Tensors it should update.
learning_rate = 1e-3
optimizer = torch.optim.RMSprop(model.parameters(), lr=learning_rate)
for t in range(2000):
    # Forward pass: compute predicted y by passing x to the model.
    y_pred = model(xx)

    # Compute and print loss.
    loss = loss_fn(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())


# Before the backward pass, use the optimizer object to zero all of the gradients
# for the variables it will update (which are the learnable weights of the model).
# This is because by default, gradients are accumulated in buffers(i.e., not overwritten) whenever .backward()
# is called. Checkout docs of torch.autograd.backward for more details.
optimizer.zero_grad()


# Backward pass: compute gradient of the loss with respect to model parameters.
loss.backward()

# Calling the step function on an Optimizer makes an update to its parameters.
optimizer.step()

linear_layer = model[0]
print(f"Result: y = {linear_layer.bias.item()} + {linear_layer.weight[:, 0].item()} x + {linear_layer.weight[:, 1].item()} x^2 + {linear_layer.weight[:,2].item()} x^3")



# PyTorch: Custom nn Modules
# Sometimes you will want to specify models that are more complex than a sequence of existing Modules;
# for these cases you can define your own Modules by subclassing nn.Module and defining a fowrard which
# receives input Tensors and produces output Tensors using other modules or other autograd operations on Tensors.
# In this example we implement our third order polynomial as a custom Modules subclass:


import torch
import math


class Polynomial3(torch.nn.Module):
    def __init__(self):
        """
        In the constructor we instantiate four parameters and assign them as member parameters.
        """
        super().__init__()
        self.a = torch.nn.Parameter(torch.randn(()))
        self.b = torch.nn.Parameter(torch.randn(()))
        self.c = torch.nn.Parameter(torch.randn(()))
        self.d = torch.nn.Parameter(torch.randn(()))

    
    def forward(self, x):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        return self.a + self.b * x + self.c * x ** 2 + self.d * x ** 3
    

    def string(self):
        """
        Just like any class in Python, you can also define custom method on PyTorch modules.
        """
        return (f"y = {self.a.item()} + {self.b.item()} x + {self.c.item()} x^2 + {self.d.item()} x^3")
    


# Create Tensors to hold input and outputs.
x = torch.linspace(-math.pi, math.pi, 2000)
y = torch.sin(x)


# Construct our model by instantiating the class defined above.
model = Polynomial3()


# Construct our loss function and an Optimizer.
# The call to model.parameters() in the SGD constructor will contain the learnable paramters
# (defined with torch.nn.Parameter) which are members of the model.

criterion = torch.nn.MSELoss(reduction='sum')
optimizer = torch.optim.SGD(model.parameters(), lr=1e-6)
for t in range(2000):
    # Forward pass: Compute predicted y by passing x to the model.
    y_pred = model(x)

    # Compute and print loss.
    loss = criterion(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())

    # Zero gradients, perform a backward pass, and update the weights.
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


print(f"Result: {model.string()}")



# PyTorch: Control Flow + Weight Sharing
# As an example of dynamic grpahs and weight sharing, we implement a very strange model:
# a third-fifth order polynomial that on each forward pass chooses a random number between
# 3 and 5 uses that many orders, reusing the same weights multiple times to compute the fourth and fifth order.
#
# For this model we can use normal Python flow control to implement the loop, and we can implement weight sharing
# by simply reusing the same parameter multiple times when defining the foward pass.
# We can easily implement this model as a Module subclass.

import random
import torch
import math

class DynamicNet(torch.nn.Module):
    def __init__(self):
        """
        In the constructor we instantiate five parameters and assign them as members.
        """
        super().__init__()
        self.a = torch.nn.Parameter(torch.randn(()))
        self.b = torch.nn.Parameter(torch.randn(()))
        self.c = torch.nn.Parameter(torch.randn(()))
        self.d = torch.nn.Parameter(torch.randn(()))
        self.e = torch.nn.Parameter(torch.randn(()))

    def forward(self, x):
        """
        For the forward pass of the model, we randomly choose either 4, 5 and reuse the e parameter
        to compute the contribution of these orders.

        Since each forward pass builds a dynamic computation graph, we can use normal Python control-flow
        operators like loops or conditional statements when defining the foward pass of the model.

        Here we also see that it is perfectly safe to reuse the same parameter many times when defining a computational graph.
        """

        y = self.a + self.b * x + self.c * x ** 2 + self.d * x ** 3
        for exp in range(4, random.randint(4, 6)):
            y = y + self.e * x ** exp
        return y
    

    def string(self):
        """
        Just like any class in Python, you can also define custom method on PyTorch modules.
        """
        return (f"y = {self.a.item()} + {self.b.item()} x + {self.c.item()} x^2 + {self.d.item()} x^3 + {self.e.item()} x^4 ? + {self.e.item()} x^5 ?")
    

# Create Tensors to hold input and outputs.
x = torch.linspace(-math.pi, math.pi, 2000)
y = torch.sin(x)


# Construct our model by instantiating the class defined above.
model = DynamicNet()

# Construct our loss function and an Optimizer.
# Training this strange model with vanilla stochastic gradient descent is tough,
# so we use momentum.
criterion = torch.nn.MSELoss(reduction='sum')
optimizer = torch.optim.SGD(model.parameters(), lr=1e-8, momentum=0.9)
for t in range(30000):
    # Forward pass: Compute predicted y by passing x to the model.
    y_pred = model(x)

    # Compute and print loss.
    loss = criterion(y_pred, y)
    if t % 2000 == 1999:
        print(t, loss.item())

    # Zero gradients, perform a backward pass, and update the weights.
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print(f"Result: {model.string()}")

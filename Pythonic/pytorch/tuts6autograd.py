# Automatic Differentiation

# When training neural networks the most frequently used algorithm is back propogation.
# In this algorithm, parameters (model weights) are adjusted according to the gradient
# of the loss function with respect to the given parameter.
# To compute those gradients, PyTorch has a built-in differentiation engine called torch.autograd .
# Consider the simplest one-layer neural network, with input x, parameters w and b, and some loss function.

# https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html


import torch

x = torch.ones(5)
y = torch.zeros(3)
w = torch.randn(5, 3, requires_grad=True)
b = torch.randn(3, requires_grad=True)
z = torch.matmul(x, w)+b
loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y)

# A function that we apply to tensors to construct computational graph is in fact an object of class Function.
# This object knows how to compute the function in the forward direction,
# and also how to compute its derivative during the backward propagation step.
# A reference to the backward propagation function is stored in grad_fn property of a tensor.

print(f"Gradient function for z = {z.grad_fn}")
print(f"Gradient function for loss = {loss.grad_fn}")


# Computing Gradients
# To optimize weights of parameters in the neural network, we need to compute the derivatives
# of our loss function with respect to parameters, namely, we need a (derivative ∂ of loss / derivative ∂ of w) and (derivative ∂ of loss / derivative ∂ of b)
# under some fixed values of x and y.
# To compute those derivatives, we call loss.backward(), and then retrieve the values from w.grad and b.grad.

loss.backward()
print(w.grad)
print(b.grad)


# Disabling Gradient Tracking
# By default, all tensors with requires_grad=True are tracking their computational history and support gradient computation.
# We do not need to do that in cases of applying a trained model to some input data.
# We only want to do forward computations through the network.
# We can stop tracking computations by surrounding our computation code with torch.no_grad() block.

z = torch.matmul(x, w)+b
print(z.requires_grad)

with torch.no_grad():
    z = torch.matmul(x, w)+b
print(z.requires_grad)


# An alternate way to achieve the same result with the detach method on the tensor.
z = torch.matmul(x, w)+b
z_det = z.detach()
print(z_det.requires_grad)


# Computational Graph
# Conceptually, autograd keeps a record of data (tensors) and all executed operations
# (along with the resulting new tensors) in a directed acyclic graph (DAG) consisting
# of Function objects. In this DAG, leaves are the input tensors, roots are the output tensors.
# By tracing this graph from roots to leaves, you can automatically compute the gradients using the chain rule.
# Instead of computing the Jacobian matrix itself, PyTorch allows you to compute
# Jacobian Product (v^T * J) for a given input vector, V == (V.1 ... V.m).
# This is achieved by calling backward with v as an argument.
# This size of V should be the same as the size of the original tensor, with which we want to compute the product:

inp = torch.eye(4, 5, requires_grad=True)
out = (inp+1).pow(2).t()
out.backward(torch.ones_like(out), retain_graph=True)
print(f"First call\n {inp.grad}")
out.backward(torch.ones_like(out), retain_graph=True)
print(f"\nSecond call\n{inp.grad}")
inp.grad.zero_()
out.backward(torch.ones_like(out), retain_graph=True)
print(f"\nCall after zeroing gradients\n{inp.grad}")


# Notice that when we call backward for the second time with the same argument,
# the value of the gradient is different. This happens because when doing backward
# propagation, PyTorch accumulates the gradients, i.e. the value of computed gradients
# is added to the grad property of all leaf nodes of computational graph.
# If you want to compute the proper gradients, you need to zero out the grad property before.
# In real-life training an optimizer helps us to do this.


# Tensors
# https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html


import torch
import numpy as np


# Initializing a Tensor
# Tensors can be initialized in various ways.

# Directly from data.
# Tensors can be created directly from data.
# The data type is automatically inferred.

data = [[1, 2], [3, 4]]
x_data = torch.tensor(data)



# From a NumPy array.
# Tensors can be created from NumPy arrays.

np_array = np.array(data)
x_np = torch.from_numpy(np_array)



# From another tensor.
# The new tensor retains the properties (shape, datatype)
# of the argument tensor, unless explicitly overridden.

x_ones = torch.ones_like(x_data)
print(f"Ones Tensor: \n {x_ones} \n")

x_rand = torch.rand_like(x_data, dtype=torch.float)
print(f"Random Tensor: \n {x_rand} \n")



# With random or constant values.
# The tuple, shape, determines the dimensionality of the
# output tensor.

shape = (2,3,)
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape)
zeros_tensor = torch.zeros(shape)

print(f"Random Tensor: \n {rand_tensor} \n")
print(f"Ones Tensor: \n {ones_tensor} ] \n")
print(f"Zeros Tensor: \n {zeros_tensor}")



# Attributes of a Tensor
# Tensor attributes describe their shape, datatype, and
# the device on which they are stored.

tensor = torch.rand(3,4)

print(f"Shape of tensor: {tensor.shape}")
print(f"Datatype of tensor: {tensor.dtype}")
print(f"Device tensor is stored on: {tensor.device}")



# Operations on Tensors
# By default, tensors are created on the CPU.
# We need to explicitly move tensors to the accelerator
# using .to method (after checking for accelerator availability).
# We move our tensor to the current accelerator if available.

if torch.accelerator.is_available():
    tensor = tensor.to(torch.accelerator.current_accelerator())



# Standard numpy-like indexing and slicing.

tensor = torch.ones(4, 4)
print(f"First row: {tensor[0]}")
print(f"First column: {tensor[:, 0]}")
print(f"Last column: {tensor[..., -1] }")
tensor[:,1] = 0
print(tensor)



# Joining tensors
# You can use torch.cat to concatenate a sequence of tensors
# along a given dimension.
# Another tensor joining operator that is subtly different
# from torch.cat.

t1 = torch.cat([tensor, tensor, tensor], dim=1)
print(t1)



# Arithmetic operations
# This computes the matrix multiplication between two tensors.
# y1, y2, y3 will have the same value ''tensor.T'' returns the
# transpose of a tensor.

y1 = tensor @ tensor.T
y2 = tensor.matmul(tensor.T)

y3 = torch.rand_like(y1)
torch.matmul(tensor, tensor.T, out=y3)


# This computes the element-wise product.
# z1, z2, z3 will have the same value.
z1 = tensor * tensor
z2 = tensor.mul(tensor)

z3 = torch.rand_like(tensor)
torch.mul(tensor, tensor, out=z3)



# Single-element tensors.
# If you have a one-element tensor, for example by aggregating
# all values of a tensor into one value, you can convert
# it to a Python numerical value using item().

agg = tensor.sum()
agg_item = agg.item()
print(agg_item, type(agg_item))



# In-place operations.
# Operations that store the result into the operand are called in-place. 
# In-place operations are denoted with a _ suffix.
# For example: x.copy_(y), x.t_() will change x.

print(f"{tensor} \n")
tensor.add_(5)
print(tensor)



# Bridge with NumPy
# Tensors on the CPU and NumPy arrays can share their underlying memory locations.
# Changing one will change the other.
print("Bridge with NumPy \n")
print("Tensor to NumPy array \n")

t = torch.ones(5)
print(f"t: {t}")
n = t.numpy()
print(f"n: {n}")


# A change in the tensor reflects in the NumPy array.

t.add_(1)
print(f"t: {t}")
print(f"n: {n}")



# NumPy Array to Tensor

n = np.ones(5)
t = torch.from_numpy(n)


# Changes in the NumPy array reflects in the tensor.

np.add(n, 1, out=n)
print(f"t: {t}")
print(f"n: {n}")


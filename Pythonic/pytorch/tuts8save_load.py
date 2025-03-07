# Save and Load the Model
# In this section we will look at how to persist model state with saving,
# loading, and running model predictions.
# https://pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html
# Note:: This approach uses Python pickle module when serializing the model,
# thus it relies on the actual class definition to be available when loading the model.
# https://docs.python.org/3/library/pickle.html


import torch
import torchvision.models as models



# Saving and Loading Model Weights
# PyTorch models store the learned parameters in an internal state dictionary called state_dict.
# These can be persisted via the torch.save method:

model = models.vgg16(weights='IMAGENET1K_V1')
torch.save(model.state_dict(), 'model_weights.pth')



# To load model weights, you need to create an instance of the same model first.
# Then load the parameter using laod_state_dict() method.
# In the code below, we set weights_only=True to limit the functions executed during
# unpickling to only those necessary for loading weights.
# Using weights_only=True is considered a best practice when loading weights.


# Instead of specifying weights, create an untrained model.
model = models.vgg16()
model.load_state_dict(torch.load('model_weights.pth', weights_only=True))

# Call model.eval() before inferencing to set the dropout and batch normalization layers
# to evaluation mode. Failing to do this will yield inconsistent inference results.
model.eval()


# Saving and Loading Models with Shapes
# When loading model weights, we needed to instantiate the model class first.
# The class defines the structure of a network.
# We might want to save the structure of this class together with the model.
# In that case, we can pass model and not model.state_dict() to the saving function.

torch.save(model, 'model.pth')


# As described in Saving and Loading torch.nn.Modules saving state_dict is
# considered the best practice. However, below we use weights_only=False because this
# involves loading the model, which is a legacy use case for torch.save.

model = torch.load('model.pth', weights_only=False)


# Loading an nn.Module from a Checkpoint
# If you're loading a checkpoint and and want to reduce compute and memory
# as much as possible, this tutorial shares some recommended practices.
# In particular, we will discuss:
#   1. The mmap keyword argument on torch.load
#   2. The torch.device() context manager
#   3. The assign keyword argument on nn.Module.load_state_dict()
# https://pytorch.org/tutorials/recipes/recipes/module_load_state_dict_tips.html?highlight=loading%20nn%20module%20from%20checkpoint

# Let us consider a simple nn.Module that contains a list of Linear layers.

import torch
from torch import nn
import time

class SomeModule(torch.nn.Module):
    def __init__(self, size):
        super().__init__()
        self.linears = nn.ModuleList([nn.Linear(size, size) for i in range(10)])

    def forward(self, x):
        return self.linears(x)
    

m = SomeModule(1000)
torch.save(m.state_dict(), 'checkpoint.pth')



# The following snippet demonstrates the use of the mmap keyword argument to torch.load,
# the torch.device() context manager and the assign keyword argument to nn.Module.load_state_dict().

state_dict = torch.load('checkpoint.pth', mmap=True, weights_only=True)
with torch.device('meta'):
    meta_m = SomeModule(1000)
meta_m.load_state_dict(state_dict, assign=True)



# Compare the snippet below to the one above:

state_dict = torch.load('checkpoint.pth', weights_only=True)
m = SomeModule(1000)
m.load_state_dict(state_dict)



# The second example does not use any of the features listed above and will be less
# compute and memory efficient for loading a checkpoint.
# In the following sections, we will discuss each of the features in further detail.



# Using torch.load(mmap=True)
# First, let us consider what happens when we load the checkpoint with torch.load.
# When we save a checkpoint with torch.save, tensor storages are tagged with the
# device they are saved on. With torch.load, tensor storages will be loaded to the
# device they were tagged with (unless this behavior is overridden using the map_location flag).
# For ease of explanation, let us assume that the tensors were saved on CPU.
# This means that on the first line all tensor storages will be loaded into CPU RAM,
# which can be undesirable when:
#   * CPU RAM is smaller than the size of the checkpoint.
#   * Waiting for the entire checkpoint to be loaded into RAM before performing,
#     for example, some per-tensor processing.

start_time = time.time()
state_dict = torch.load('checkpoint.pth', weights_only=True)
end_time = time.time()

print(f"loading time without mmap={end_time - start_time}")



# The mmap keyword argument to torch.load attempts to solve the above two problems.
# As its name implies, the mmap keyword argument to torch.load makes use of an mmap call
# which maps a file on disk into virtual memory and lets the OS hadnle loading and unloading
# into physical memory automatically. When this flag is passed, tensor storages will be memory-mapped.

start_time = time.time()
state_dict = torch.load('checkpoint.pth', mmap=True, weights_only=True)
end_time = time.time()
print(f"loading time with mmap={end_time - start_time}")



# As mentioned above, one can use this argument to do per-tensor processing on a
# checkpoint without loading all tensor storages into CPU memory upfront.

def my_special_routine(t, device):
    # This could be a much fancier operation.
    return t.to(dtype=torch.bfloat16, device=device)

def my_processing_function(key, device):
    t = state_dict[key]
    processed_t = my_special_routine(t, device)
    del t
    state_dict[key] = processed_t

for key in state_dict.keys():
    device = torch.device('cpu')
    my_processing_function(key, device)



# Using torch.device('meta)
# Next, let's consider the creation of the module.

m = SomeModule(1000)


# This allocates memory for all parameters/buffers and initializes
# them per the default initialization schemes defined in SomeModule.__init__(),
# which is wasteful when we want to load a checkpoint for the following reasons:
#   * The result of the initialization kernels will be overwritten by load_state_dict()
#     without ever being used, so initializaiton is wasteful.
#   * Allocate memory for these parameters/buffers in RAM while torch.load of the saved
#     state dictionary also allocates memory in RAM for parameters/buffers in the checkpoint.

# In order to solve these two problems, we can use the torch.device() context manager
# with device='meta' when we instantiate the nn.Module().

# The torch.device() context manager makes sure that factory calls will be performed
# as if they were passed the specified device as an argument.
# Tensors on torch.device('meta') do not carry data.
# However, they possess all other metadata a tensor carries such as:
#   * .size()
#   * .stride()
#   * .requires_grad

with torch.device('meta'):
    new_m = SomeModule(1000)



# Using load_state_dict(assign=True)
# Next, we consider the loading of the state dictionary.

m.load_state_dict(state_dict)


# An in-place copy into a tensor on the meta device is no-op.
# In order to avoid this, we can pass the assign=True keyword argument to load_state_dict().
# A caveat here is that since optimizers hold a reference to nn.Module.parameters()
# the optimizer must be initialized after the module is loaded from state dict if
# assign=True is passed. As of PyTorch 2.3.0, one can use to avoid this caveat.

new_m.load_state_dict(state_dict, assign=True)


# Before 2.3.0, this MUST be done AFTER the load_state_dict with assign.
# In versions >= 2.3.0, 
# one can consider setting torch.__future__.set_swap_module_params_on_conversion
opt = torch.optim.SGD(new_m.parameters(), lr=1e-3)



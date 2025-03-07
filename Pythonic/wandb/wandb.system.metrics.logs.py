# ./wandb/wandb.system.metrics.logs.py

import wandb
import random

# Start a new wandb run to track this script.
wandb.init(
    # Set the wandb project where this run will be logged.
    project="wandb.system.metrics.logs",

    # Track hyperparameters and run metadata.
    config={
        "learning_rate": 0.02,
        "architecture": "CNN",
        "dataset": "CIFAR-100",
        "epochs": 10,
    }

)

# Simulate training.
epochs = 10
offset = random.random() / 5
for epoch in range(2, epochs):
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch - random.random() /epoch + offset


    # Log metrics to wandb.
    wandb.log({"acc": acc, "loss": loss})


# [optional] finish the wandb run, necessary in notebooks.
wandb.finish()
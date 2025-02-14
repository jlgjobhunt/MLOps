# ./MLOps/dvc/dvc.install.test0.py

import pandas as pd
import subprocess

# 1. Create a simple CSV file (data.csv) - this will be versioned by DVC.
data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)

# Add to DVC
subprocess.run(["dvc", "add", "data.csv"], check=True)

# Commit to Git
subprocess.run(["git", "add", "data.csv.dvc"], check=True)
subprocess.run(["git", "commit", "-m", "Added initial data."], check=True)

print("dvc.install.test0.py completed")

# 5. (Optional) Create a simple pipeline stage (if needed for your test)
# For example, create a process.py file that does some transformation:
# # process.py

import pandas as pd
import sys

input_file = sys.argv[1] # Get input from command line.
output_file = sys.argv[2] # Get output from command line.

df = pd.read_csv(input_file)
df['col3'] = df['col1'] * 2
df.to_csv(output_file, index=False)

print("dvc.install.test1.py completed!")


# Add this file to dvc pipeline using the dvc.yaml
# See the dvc.yaml file in this directory.
# dvc repro process_data
# Previous command refers to process_data in dvc.yaml file.

# 6. Now, in your Python script (this script):
# try:
#   # Read the data using dvc.api (this confirms DVC is working).
#   # If using a specific version, include `rev=<git_commit_hash>'`
#    data_path = 'data.csv' # Or 'processed_data.csv' if you have a pipeline.
#    data_url = dvc.api.get_url(data_path) # Get URL for the data.
#    print(f"Data URL: {data_url}")

#    df_from_dvc = pd.read_csv(dvc.api.read(data_path))
#    print("Data loaded from DVC:")
#    print(df_from_dvc)

    # If you have a pipeline, you can get the processed data:
#    processed_data = pd.read_csv(dvc.api.read('processed_data.csv'))
#    print("\nProcessed Data loaded from DVC:")
#    print(processed_data)

# except Exception as e:
#   print(f"Error: {e}")
#    print("DVC might not be properly configured or the data file might not be tracked.")





# 7. (Optional) Push your data to a remote storage (if configured)
# dvc remote add -d myremote s3://my-dvc-bucket
# dvc push
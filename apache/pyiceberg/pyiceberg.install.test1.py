# ./MLOps/apache/pyiceberg/pyiceberg.install.test1.py

# Pyiceberg without usage of integrations with pyspark,
# pandas, duckdb, nor cloud providers.
# In pyiceberg version 0.9.0 there is a different support level for:
# pyiceberg.data
# pyiceberg.utils.manifest
# from pyiceberg.utils.schema_conversion import convert_schema
# from pyiceberg.catalog import load_catalog (* - uses properties dict instead of 2 positional arguments)
# from pyiceberg.catalog import HadoopCatalog
# Instead use: pyiceberg.catalog import Catalog

# Necessary environmental variables to set before running this file:
#
#
#


from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import IntegerType, StringType, StructType, DateType
from pyiceberg.table import Table
from pyiceberg.io import FileIO
import uuid
import os
import json


# Configuration
catalog_name = "local"
warehouse_path = "/tmp/iceberg_warehouse"
table_name = "my_table"
table_identifier = f"{catalog_name}.default.{table_name}"
manifest_list_location = f"{warehouse_path}/default/{table_name}/metadata/manifest_list.json"


# Create a catalog
catalog = load_catalog(catalog_name)


# Define a schema
schema = Schema(
    StructType(
        [
            IntegerType().field("id"),
            StringType().field("name"),
            DateType().field("date"),
        ]
    )
)

# Create a table
if table_identifier not in catalog.list_tables("default"):
    table = catalog.create_table(table_identifier, schema)
else:
    table = catalog.load_table(table_identifier)

# Write data (manually create a manifest file)
manifest_file = f"{warehouse_path}/default/{table_name}/data/manifest-{uuid.uuid4()}.json"
data_file = f"{warehouse_path}/default/{table_name}/data/data-{uuid.uuid4()}.parquet"

# Manually simulate writing a parquet file
# Use actual parquet data in a real scenario.
with open(data_file, "w") as f:
    f.write("Simulated Parquet Data")

# Create a manifest entry manually.
manifest_entry = {
    "status": 1, # ADDED
    "snapshot_id": table.current_snapshot().snapshot_id if table.current_snapshot() else None,
    "data_file": {
        "file_path": data_file,
        "file_format": "PARQUET",
        "record_count": 3, # Replace with actual count
        "file_size_in_bytes": os.path.getsize(data_file),
        "value_counts": {"id": 3, "name": 3, "date": 3},
        "null_value_counts": {"id": 0, "name": 0, "date": 0},
        "lower_bounds": {"id": 1, "name": "A", "date": "2025-02-01"},
        "upper_bounds": {"id": 3, "name": "C", "date": "2025-03-06"},
    },
}

# Manually write the manifest file as JSON
with open(manifest_file, "w") as f:
    json.dump({"entries": [manifest_entry]}, f)

# Update the table's metadata
table.append_files([manifest_file])
table.refresh()

# Read the table's metadata
current_snapshot = table.current_snapshot()
manifest_list = current_snapshot.manifest_list
manifest_list_file = FileIO(None).open(manifest_list)

# Print metadata
print(f"Current Snapshot ID: {current_snapshot.snapshot_id}")
print(f"Manifest List Location: {manifest_list}")

# Cleanup
if os.path.exists(data_file):
    os.remove(data_file)
if os.path.exists(manifest_file):
    os.remove(manifest_file)
if os.path.exists(manifest_list_location):
    os.remove(manifest_list_location)
if os.path.exists(f"{warehouse_path}/default/{table_name}/metadata/version-1.json"):
    os.remove(f"{warehouse_path}/default/{table_name}/metadata/version-1.json")
if os.path.exists(f"{warehouse_path}/default/{table_name}/metadata/v1.metadata.json"):
    os.remove(f"{warehouse_path}/default/{table_name}/v1.metadata.json")
if os.path.exists(f"{warehouse_path}/default/{table_name}/metadata"):
    os.rmdir(f"{warehouse_path}/default/{table_name}/metadata")
if os.path.exists(f"{warehouse_path}/default/{table_name}/data"):
    os.rmdir(f"{warehouse_path}/default/{table_name}/data")
if os.path.exists(f"{warehouse_path}/default/{table_name}"):
    os.rmdir(f"{warehouse_path}/default/{table_name}")
if os.path.exists(f"{warehouse_path}/default"):
    os.rmdir(f"{warehouse_path}/default")


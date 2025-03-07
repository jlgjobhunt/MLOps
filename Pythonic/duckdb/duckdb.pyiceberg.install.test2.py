# ./MLOps/duckdb/duckdb.pyiceberge.install.test2.py

import duckdb
import os

# Configuration
warehouse_path = "/tmp/iceberg_090_duckdb"
table_name = "my_090_duckdb_table"
table_path = f"{warehouse_path}/default/{table_name}"

# DuckDB Connection
duckdb_con = duckdb.connect()


# Install and load the DuckDB Iceberg Extension
duckdb_con.execute("INSTALL iceberg")
duckdb_con.execute("LOAD iceberg")


# Create a DuckDB table.
duckdb_con.execute(
    f"""
    CREATE OR REPLACE TABLE data AS SELECT 1 as id, 'Joshua' as name, CAST('2025-03-06' AS DATE) as date_col UNION ALL
    SELECT 2, 'Barbara', CAST('2025-03-06' AS DATE) as date_col UNION ALL
    SELECT 3, 'Catherine', CAST('2025-03-06' AS DATE) as date_col
    """
)

# Write to Iceberg using DuckDB
duckdb_con.execute(f"COPY data TO '{table_path}' (FORMAT ICEBERG, MODE CREATE_OR_REPLACE)")

# Query the Iceberg table using DuckDB
result = duckdb_con.execute(f"SELECT * FROM '{table_path}'").fetchall()
print(result)

# Cleanup
duckdb_con.close()

if os.path.exists(f"{warehouse_path}/default/{table_name}/data"):
    for file in os.listdir(f"{warehouse_path}/default/{table_name}/data"):
        os.remove(f"{warehouse_path}/default/{table_name}/data/{file}")

if os.path.exists(f"{warehouse_path}/default/{table_name}/metadata"):
    for file in os.listdir(f"{warehouse_path}/default/{table_name}/metadata"):
        os.remove(f"{warehouse_path}/default/{table_name}/metadata/{file}")

if os.path.exists(f"{warehouse_path}/default/{table_name}"):
    os.rmdir(f"{warehouse_path}/default/{table_name}")

if os.path.exists(f"{warehouse_path}/default"):
    os.rmdir(f"{warehouse_path}/default")


# ./MLOps/duckdb/duckdb.install.test0.py

try:
    import duckdb
    print("DuckDB has been installed.")

except ImportError as e:
    print(f"Installation failed: {e}")


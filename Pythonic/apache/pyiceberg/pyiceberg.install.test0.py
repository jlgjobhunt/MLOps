# ./MLOps/apache/pyiceberg/pyiceberg.install.test0.py

try:
    import pyiceberg
    print("Apache Iceberg (pyiceberg) has been installed and doesn't rely upon the JVM.")

except ImportError as e:
    print(f"Installation failed: {e}")


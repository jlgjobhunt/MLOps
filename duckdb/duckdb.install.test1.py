# ./MLOps/duckdb/duckdb.install.test1.py

import duckdb

# 1. Create a DuckDB database.

# File based.
con = duckdb.connect(database="install.test1.duckdb")

# In-memory: con = duckdb.connect()

# 2. Handle state of table existence from prior DDL session.
table_exists = con.execute(
    "SELECT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'employees')"
).fetchone()[0]

if not table_exists:

    # 3. Create a table.
    con.execute("""
        CREATE TABLE employees (
            id INTEGER,
            name VARCHAR,
            salary DECIMAL,
            department VARCHAR,
        )
    """)
    print("Table 'employees' created.")
else:
    print("Table 'employees' already exists.")

# 4. Inserting Data
con.execute("INSERT INTO employees VALUES (1, 'Alison', 60000.00, 'Sales')")
con.execute("INSERT INTO employees VALUES (2, 'Boyd', 75000.00, 'Marketmaking')")
con.execute("INSERT INTO employees VALUES (3, 'Caroline', 90000.00, 'Engineering')")
con.execute("INSERT INTO employees VALUES (4, 'Dave', 120000.00, 'Legal')")


# 5. Query data

# Query data
result = con.execute("SELECT * FROM employees").fetchall()
print("All employees:", result)


# Filtered query
engineering_employees = con.execute("SELECT * FROM employees WHERE department = 'Engineering'").fetchall()
print("Engineering employees:", engineering_employees)


# Aggregated query
average_salary = con.execute("SELECT AVG(salary) FROM employees").fetchone()[0]
print("Average salary:", average_salary)


# 6. Basic Data Analysis

# Simple Analysis
max_salary = con.execute("SELECT MAX(salary) FROM employees").fetchone()[0]
print("Maximum salary:", max_salary)

department_salaries = con.execute("SELECT department, AVG(salary) FROM employees GROUP BY department").fetchall()
print("Average salaries by department:", department_salaries)


# 7. Exporting Data

# Export data to a CSV file.
con.execute("COPY (SELECT * FROM employees) TO 'employees.csv' (HEADER, DELIMITER ',')")
print("Data exported to employees.csv")

# Export data to a parquet file.
con.execute("COPY (SELECT * FROM employees) TO 'employees.parquet' (FORMAT PARQUET)")
print("Data exported to employees.parquet")


# 8. Close the connection.
con.close()
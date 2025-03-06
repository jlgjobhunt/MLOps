# ./MLOps/apache/pyspark/pyspark.install.test1.py

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType, LongType
from pyspark.sql.functions import col, avg, max, min, when, udf, year
import datetime
import logging

# Configure logging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pyspark_exercise():
    """Demonstrates various PySpark functionalities."""

    # Begin Logging
    logging.info("Starting SparkSession.")

    try:
                
        # Intialize SparkSession
        spark = SparkSession.builder.appName("PySparkExercise").getOrCreate()


        # 1. Define a Schema.
        # As of pyspark 3.5.5 there is no support for double in pyspark.sql.functions.
        # There are issues with schema inference and type casting between double and long.

        schema = StructType([
            StructField("name", StringType(), True),
            StructField("age", LongType(), True),
            StructField("occupation", StringType(), True),
            StructField("salary", DoubleType(), True),
            StructField("date of hire", DateType(), True)
        ])


        # 2. Create a DataFrame
        data = [
            ("God", 14000000000, "God", 888.888, datetime.date(5987, 8, 9)),
            ("Adam", 930, "Made Man", 0.0, datetime.date(4004, 8, 9)),
            ("Seth", 912, "Spritualist", 0.0, datetime.date(3874, 8, 9)),
            ("Abraham", 175, "Freelance Adventurer", 40000.0, datetime.date(1900, 3, 5)),
            ("Joshua Greenfield", 42, "Business & Engineering Consultant", 350000.0, datetime.date(1983, 8, 9)),
            ("Alice", 25, "Engineer", 60000.0, datetime.date(2018, 10, 15)),
            ("Bob", 30, "Analyst", 75000.0, datetime.date(2018, 5, 20)),
            ("Charlie", 35, "Manager", 90000.0, datetime.date(2018, 12, 10)),
            ("David", 28, "Engineer", 65000.0, datetime.date(2018, 8, 5)),
            ("Eve", 32, "Analyst", 80000.0, datetime.date(2018, 3, 25)),
            ("Frank", 40, "Manager", 100000.0, datetime.date(2021, 6, 30)),
            ("Grace", 27, "Engineer", 62000.0, datetime.date(2021, 11, 12)),
            ("Henry", 33, "Analyst", 82000.0, datetime.date(2021, 2, 18)),
            ("Ivy", 38, "Manager", 95000.0, datetime.date(2021, 9, 7)),
            ("Jack", 29, "Engineer", 68000.0, datetime.date(2022, 7, 1))
        ]

        df = spark.createDataFrame(data, schema)

        # 3. Basic DataFrame Operations
        logging.info("Basic DataFrame Operations")
        df.show()
        df.printSchema()
        print(f"Number of rows: {df.count()}")
        logging.info(f"Number of rows: {df.count()}")

        # 4. DataFrame Transformations
        logging.info("DataFrame Transformations")
        df_transformed = df.withColumn("salary_increase", col("salary") * 1.1) \
                        .withColumn("is_manager", when(col("occupation") == "Engineer", True).otherwise(False))
        df_transformed.show()


        # 5. DataFrame Filtering
        logging.info("DataFrame Filtering")
        df.filter(col("age") > 30).show()

        # 6. DataFrame Aggregations
        logging.info("DataFrame Aggregations")
        df.groupBy("occupation").agg(avg("salary").alias("avg_salary"),
                                    max(col("age").cast("double")).alias("max_age"),
                                    min(col("age").cast("double")).alias("min_age")).show()
        
        # 7. DataFrame Sorting
        logging.info("DataFrame Sorting")
        df.orderBy("age", ascending=False).show()

        # 8. Working with Dates
        logging.info("Working with Dates")
        df_with_year = df.withColumn("hire_year", year(col("date of hire")))
        df_with_year.show()

        # 9. Writing and Reading Data (Example: CSV)
        logging.info("Writing and Reading Data (CSV)")
        temp_csv_path = "temp_data.csv"
        df.write.csv(temp_csv_path, header=True, mode="overwrite")
        df_read = spark.read.csv(temp_csv_path, header=True, inferSchema=True)
        df_read.show()

        # 10. UDF (User Defined Function)
        logging.info("UDF (User Defined Function)")
        def categorize_salary(salary):
            if salary < 70000:
                return "Low"
            elif 70000 <= salary < 90000:
                return "Medium"
            else:
                return "High"
            

        categorize_salary_udf = udf(categorize_salary, StringType())
        df_with_category = df.withColumn("salary_category", categorize_salary_udf(col("salary")))
        df_with_category.show()

        # Stop SparkSession
        spark.stop()

        # End Logging
        logging.info("SparkSession completed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    logging.info("PySpark exercise complete.")

if __name__ == "__main__":
    pyspark_exercise()
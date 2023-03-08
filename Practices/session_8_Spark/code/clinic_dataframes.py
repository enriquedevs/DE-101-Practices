from pyspark.sql import SparkSession
import psycopg2
import csv

# PostgreSQL connection parameters
conn_params = {
    "host": "postgres_db",
    "port": 5432,
    "database": "clinic_db",
    "user": "myuser",
    "password": "mypassword"
}

# Initialize Spark
spark = SparkSession.builder.appName("ClinicApp").getOrCreate()

# Read CSV file into DataFrame
csv_file = spark.read.csv("./clinic_2.csv", header=True, inferSchema=True)

# Create DataFrames for each table
patients_df = csv_file.select("patient_name", "patient_last_name", "patient_address") \
    .withColumnRenamed("patient_name", "name") \
    .withColumnRenamed("patient_last_name", "last_name")
clinical_specializations_df = csv_file.select("doctor_clinical_specialization").distinct() \
    .withColumnRenamed("doctor_clinical_specialization", "name")
doctors_df = csv_file.select("doctor_name", "doctor_last_name", "doctor_clinical_specialization") \
    .join(clinical_specializations_df, "name") \
    .select("doctor_name", "doctor_last_name", "id") \
    .withColumnRenamed("id", "clinical_specialization_id")
appointments_df = csv_file.select("patient_name", "patient_last_name", "doctor_name", "doctor_last_name", "appointment_date", "appointment_time") \
    .join(patients_df, ["name", "last_name"]) \
    .join(doctors_df, ["doctor_name", "doctor_last_name", "clinical_specialization_id"]) \
    .select("appointment_date", "appointment_time", "patient_id", "doctor_id")

# Define save functions
def save_to_postgres(df, table_name):
    df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{conn_params['host']}:{conn_params['port']}/{conn_params['database']}") \
        .option("dbtable", table_name) \
        .option("user", conn_params["user"]) \
        .option("password", conn_params["password"]) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Save DataFrames to PostgreSQL
save_to_postgres(patients_df, "patient")
save_to_postgres(clinical_specializations_df, "clinical_specialization")
save_to_postgres(doctors_df, "doctor")
save_to_postgres(appointments_df, "appointment")

# Stop Spark session
spark.stop()
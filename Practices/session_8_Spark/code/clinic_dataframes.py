from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, to_timestamp

# PostgreSQL connection parameters
conn_params = {
    "host": "postgres_db",
    "port": 5432,
    "database": "clinic_db",
    "user": "myuser",
    "password": "mypassword"
}

# Initialize Spark
spark = SparkSession.builder \
    .appName("ClinicApp") \
    .master("local[*]") \
    .config('spark.jars', './postgresql-42.5.4.jar') \
    .getOrCreate()

# Read CSV file into DataFrame
print("Reading from csv file.")
csv_df = spark.read.csv("./clinic_2.csv", header=True, inferSchema=True)

# Create DataFrames for each table
print("Initializing Dataframes.")
patient_df = csv_df.select("patient_name", "patient_last_name", "patient_address") \
    .withColumnRenamed("patient_name", "name") \
    .withColumnRenamed("patient_last_name", "last_name") \
    .withColumnRenamed("patient_address", "address")

clinical_specialization_df = csv_df.select("doctor_clinical_specialization").distinct() \
    .withColumnRenamed("doctor_clinical_specialization", "name")

doctor_df = csv_df.select("doctor_name", "doctor_last_name") \
    .withColumnRenamed("doctor_name", "name") \
    .withColumnRenamed("doctor_last_name", "last_name")

appointment_df = csv_df.select("appointment_date", "appointment_time") \
    .withColumnRenamed("appointment_date", "date") \
    .withColumnRenamed("appointment_time", "time")
appointment_df = appointment_df.select(to_date(appointment_df.date, 'yyyy-MM-dd').alias('date'), to_timestamp(appointment_df.time, 'HH:mm a').alias('time'))
    

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
print('Saving to postgres...')
save_to_postgres(patient_df, "patient")
save_to_postgres(clinical_specialization_df, "clinical_specialization")
save_to_postgres(doctor_df, "doctor")
save_to_postgres(appointment_df, "appointment")
print('Save to postgres completed!')
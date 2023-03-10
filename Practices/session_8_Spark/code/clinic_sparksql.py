from pyspark.sql import SparkSession

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

# Read CSV file and declare a Temp View clinic
print("Reading and loading a Temp View from csv file.")
spark.read.csv("./clinic_3.csv", header=True, inferSchema=True).createOrReplaceTempView("clinic")

# Create DataFrames for each table with SparkSQL
print("Initializing Dataframes with SparkSQL.")

patient_df = spark.sql('select patient_name as name, patient_last_name as last_name, patient_address as address from clinic')

clinical_specialization_df = spark.sql('select doctor_clinical_specialization as name from clinic')

doctor_df = spark.sql('select doctor_name as name, doctor_last_name as last_name from clinic')

appointment_df = spark.sql("select to_date(appointment_date, 'yyyy-MM-dd') as date, to_timestamp(appointment_time, 'HH:mm a') as time from clinic")

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
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
csv_file = spark.read.csv("./clinic_1.csv", header=True, inferSchema=True)

# Register DataFrame as temporary table
csv_file.createOrReplaceTempView("clinic")

# Define SQL queries
patients_query = "INSERT INTO patient (name, last_name, address) SELECT patient_name AS name, patient_last_name AS last_name, patient_address AS address FROM clinic"
clinical_specializations_query = "INSERT INTO clinical_specialization (name) SELECT DISTINCT doctor_clinical_specialization AS name FROM clinic"
doctors_query = "INSERT INTO doctor (name, last_name, clinical_specialization_id) SELECT doctor_name AS name, doctor_last_name AS last_name, cs.id AS clinical_specialization_id FROM clinic c JOIN clinical_specialization cs ON c.doctor_clinical_specialization = cs.name"
appointments_query = "INSERT INTO appointment (date, time, patient_id, doctor_id) SELECT appointment_date AS date, appointment_time AS time, p.id AS patient_id, d.id AS doctor_id FROM clinic c JOIN patient p ON c.patient_name = p.name AND c.patient_last_name = p.last_name JOIN doctor d ON c.doctor_name = d.name AND c.doctor_last_name = d.last_name AND c.doctor_clinical_specialization = d.clinical_specialization_id"

# Define function to execute SQL query
def execute_query(query):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

# Execute SQL queries
execute_query(patients_query)
execute_query(clinical_specializations_query)
execute_query(doctors_query)
execute_query(appointments_query)

# Stop Spark session
spark.stop()
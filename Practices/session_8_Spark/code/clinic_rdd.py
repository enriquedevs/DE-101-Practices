from pyspark import SparkConf, SparkContext
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
conf = SparkConf().setAppName("ClinicApp").setMaster("local[*]")
sc = SparkContext(conf=conf)

# Read CSV file into RDD
csv_file = sc.textFile("./clinic_1.csv")
header = csv_file.first()
data = csv_file.filter(lambda row: row != header)

# Define transformation functions
def split_row(row):
    fields = row.split(",")
    return (fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7])

def save_patient(row):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute("INSERT INTO patient (name, last_name, address) VALUES (%s, %s, %s) RETURNING id", (row[0], row[1], row[2]))
    patient_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return (patient_id, row)

def save_clinical_specialization(row):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute("INSERT INTO clinical_specialization (name) VALUES (%s) RETURNING id", (row[7],))
    clinical_specialization_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return (clinical_specialization_id, row)

def save_doctor(row):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute("INSERT INTO doctor (name, last_name, clinical_specialization_id) VALUES (%s, %s, %s) RETURNING id", (row[5], row[6], row[7]))
    doctor_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return (doctor_id, row)

def save_appointment(row):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute("INSERT INTO appointment (date, time, patient_id, doctor_id) VALUES (%s, %s, %s, %s)", (row[3], row[4], row[1], row[0]))
    conn.commit()
    cur.close()
    conn.close()
    return row

# Transform data using RDDs
transformed_data = data.map(split_row)\
    .map(save_patient)\
    .map(save_clinical_specialization)\
    .map(save_doctor)\
    .map(save_appointment)

# Collect results and print to console
results = transformed_data.collect()
print(results)
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

# Define save functions
def save_to_postgres(rdd, columns, table_name, spark):
    if table_name == 'appointment':
        df = spark.createDataFrame(rdd, columns)
        df = df.select(to_date(df.date, 'yyyy-MM-dd').alias('date'), to_timestamp(df.time, 'HH:mm a').alias('time'))
    else:
        df = spark.createDataFrame(rdd, columns)
    df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{conn_params['host']}:{conn_params['port']}/{conn_params['database']}") \
        .option("dbtable", table_name) \
        .option("user", conn_params["user"]) \
        .option("password", conn_params["password"]) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("ClinicApp") \
    .master("local[*]") \
    .config('spark.jars', './postgresql-42.5.4.jar') \
    .getOrCreate()

# Read CSV to RDD
file_rdd = spark.sparkContext.textFile('./clinic_1.csv')

print(f'file has {file_rdd.count()} rows')

print('CSV file content')
file_rdd.foreach(lambda row: print(row))

header = file_rdd.first()

# Obtaining CSV file content without the header
rows_rdd = file_rdd.filter(lambda row: row != header)

print('CSV file content without header')
rows_rdd.foreach(lambda row: print(row))

# Obtaining column values of the CSV by splitting by ','
mapped_rdd = rows_rdd.map(lambda row: row.split(','))

print('CSV file content')
mapped_rdd.foreach(lambda row: print(row))

# Obtaining individual RDDs for each table
patient_rdd = mapped_rdd.map(lambda row: [row[0], row[1], row[2]])
clinical_specialization_rdd = mapped_rdd.map(lambda row: [row[7]])
doctor_rdd = mapped_rdd.map(lambda row: [row[5], row[6]])
appointment_rdd = mapped_rdd.map(lambda row: [row[3], row[4]])

# Saving to postgresdo
print('Saving to postgres...')
save_to_postgres(patient_rdd, ['name', 'last_name', 'address'], 'patient', spark)
save_to_postgres(clinical_specialization_rdd, ['name'], 'clinical_specialization', spark)
save_to_postgres(doctor_rdd, ['name', 'last_name'], 'doctor', spark)
save_to_postgres(appointment_rdd, ['date', 'time'], 'appointment', spark)
print('Save to postgres completed!')
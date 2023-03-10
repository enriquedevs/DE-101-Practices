from pyspark import SparkConf, SparkContext

# PostgreSQL connection parameters
conn_params = {
    "host": "postgres_db",
    "port": 5432,
    "database": "clinic_db",
    "user": "myuser",
    "password": "mypassword"
}

# Define a function to return all elements except for the first one
def remove_first(iterator):
    return list(iterator)[1:]

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

# Initialize Spark
conf = SparkConf().setAppName("ClinicApp").setMaster("local[*]")
sc = SparkContext(conf=conf)

# Read CSV to RDD
file_rdd = sc.textFile('./clinic_1.csv')

print(f'file has {file_rdd.count()} rows')

print('CSV file content')
file_rdd.foreach(lambda row: print(row))

# Obtaining CSV file content without the header
rows_rdd = file_rdd.mapPartitionsWithIndex(lambda i, iterator: remove_first(iterator) if i > 0 else iterator)

print('CSV file content without header')
rows_rdd.foreach(lambda row: print(row))

# Obtaining column values of the CSV by splitting by ','
mapped_rdd = rows_rdd.map(lambda row: row.split(','))

print('CSV file content')
mapped_rdd.foreach(lambda row: print(row))

# Obtaining individual RDDs for each table
patient_rdd = mapped_rdd.map(lambda row: (row[0], row[1], row[3]))
clinical_specialization_rdd = mapped_rdd.map(lambda row: (row[7]))
doctor_rdd = mapped_rdd.map(lambda row: (row[5], row[6]))
appointment_rdd = mapped_rdd.map(lambda row: (row[3], row[4]))

# Saving to postgres
print('Saving to postgres...')
df1 = patient_rdd.toDF(['name', 'last_name', 'address'])
save_to_postgres(df1, 'patient')

print('Saved to postgres complete!')
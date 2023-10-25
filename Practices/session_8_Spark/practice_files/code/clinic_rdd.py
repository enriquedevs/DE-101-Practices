from pyspark.sql.functions import to_date, to_timestamp

from common import utils

spark = utils.get_spark_session()

# 1 READ

# 1.1 Read CSV to RDD
file_rdd = spark.sparkContext.textFile('./clinic_1.csv')

# Info
# print(f'file has {file_rdd.count()} rows')
# print('CSV file content')
# file_rdd.foreach(lambda row: print(row))

# 2 TRANSFORM

# 2.1 Get the header of the csv to `set job without header`
header = file_rdd.first()

# 2.2 Obtaining CSV file content without the header
rows_rdd = file_rdd.filter(lambda row: row != header)

# Info
# print('CSV file content without header')
# rows_rdd.foreach(lambda row: print(row))

# 2.3 Obtaining column values of the CSV by splitting by ','
mapped_rdd = rows_rdd.map(lambda row: row.split(','))

# Info
# print('CSV file content')
# mapped_rdd.foreach(lambda row: print(row))

# 2.4 Obtaining individual RDDs for each table
patient_rdd = mapped_rdd.map(lambda row: [row[0], row[1], row[2]])
clinical_specialization_rdd = mapped_rdd.map(lambda row: [row[7]])
doctor_rdd = mapped_rdd.map(lambda row: [row[5], row[6]])
appointment_rdd = mapped_rdd.map(lambda row: [row[3], row[4]])

# 3 LOAD

# 3.1 Define save function
def save_to_postgres(rdd, columns, table_name, spark):
    # Create a dataframe using the rdd
    df = spark.createDataFrame(rdd, columns)

    # The appointment table will use a different datatype (date and timestamp), if we don't do this conversion, the insert will fail
    if table_name == 'appointment':
        df = df.select(
            to_date(df.date, 'yyyy-MM-dd').alias('date'),
            to_timestamp(df.time, 'HH:mm a').alias('time'))

    # Write the dataframe into db
    utils.df_write(df, table_name)

# 3.2 Call function for each table
# print('Saving to postgres...')
save_to_postgres(patient_rdd, ['name', 'last_name', 'address'], 'patient', spark)
save_to_postgres(clinical_specialization_rdd, ['name'], 'clinical_specialization', spark)
save_to_postgres(doctor_rdd, ['name', 'last_name'], 'doctor', spark)
save_to_postgres(appointment_rdd, ['date', 'time'], 'appointment', spark)
# print('Save to postgres completed!')

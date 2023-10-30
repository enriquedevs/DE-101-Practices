from pyspark.sql.functions import to_date, to_timestamp

from common import utils

spark = utils.get_spark_session()

# 1 READ

# 1.1 Read CSV file into DataFrame
# print("Reading from csv file.")
csv_df = spark.read.csv("./clinic_2.csv", header=True, inferSchema=True)

# 2 TRANSFORM

# 2.1 Create dataframes for each table
# print("Initializing Dataframes.")
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

# 3 LOAD

# 3.1 Save DataFrames to PostgreSQL
# print('Saving to postgres...')
utils.df_write(patient_df, "patient")
utils.df_write(clinical_specialization_df, "clinical_specialization")
utils.df_write(doctor_df, "doctor")
utils.df_write(appointment_df, "appointment")
# print('Save to postgres completed!')

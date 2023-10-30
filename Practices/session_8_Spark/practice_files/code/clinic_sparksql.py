from common import utils

spark = utils.get_spark_session()

# 1 READ

# 1.1 Read CSV file into DataFrame
# print("Reading from csv file.")
# print("Reading and loading a Temp View from csv file.")
spark.read.csv("./clinic_3.csv", header=True, inferSchema=True).createOrReplaceTempView("clinic")

# 2 TRANSFORM

# 2.1 Create dataframes for each table
# print("Initializing Dataframes.")
# print("Initializing Dataframes with SparkSQL.")
patient_df = spark.sql('select patient_name as name, patient_last_name as last_name, patient_address as address from clinic')
clinical_specialization_df = spark.sql('select doctor_clinical_specialization as name from clinic')
doctor_df = spark.sql('select doctor_name as name, doctor_last_name as last_name from clinic')
appointment_df = spark.sql("select to_date(appointment_date, 'yyyy-MM-dd') as date, to_timestamp(appointment_time, 'HH:mm a') as time from clinic")

# 3 LOAD

# 3.1 Save DataFrames to PostgreSQL

# print('Saving to postgres...')
utils.df_write(patient_df, "patient")
utils.df_write(clinical_specialization_df, "clinical_specialization")
utils.df_write(doctor_df, "doctor")
utils.df_write(appointment_df, "appointment")
# print('Save to postgres completed!')

from pyspark.sql import SparkSession

# PostgreSQL connection parameters
pg_params = {
    "host": "postgres_db",
    "port": 5432,
    "database": "clinic_db",
    "user": "myuser",
    "password": "mypassword"
}

# Spark session builder
def get_spark_session():
  return SparkSession.builder \
    .appName("ClinicApp") \
    .master("local[*]") \
    .config('spark.jars', './postgresql-42.5.4.jar') \
    .getOrCreate()

# Writes a dataframe into the postgres instance
def df_write(df, table_name):
    df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{pg_params['host']}:{pg_params['port']}/{pg_params['database']}") \
        .option("dbtable", table_name) \
        .option("user", pg_params["user"]) \
        .option("password", pg_params["password"]) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
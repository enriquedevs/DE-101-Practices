import requests
from pyspark.sql import SparkSession
from pyspark import SparkContext
import pandas as pd

# set up the Spark session
# spark = SparkSession.builder.appName("WeatherData").getOrCreate()
sc = SparkContext("local", "first app")
spark = SparkSession(sc)

# specify the API endpoint and parameters
# https://openweathermap.org API
url = "https://api.openweathermap.org/data/2.5/forecast"
params = {"q": "London,uk", "appid": "548d59595fe968f8291def241ba03f46"}

# make the API request and parse the response as json
response = requests.get(url, params=params)
data = response.json()

# create a Spark DataFrame from the response data
rddjson = sc.parallelize([data])
#rddjson1 = sc.parallelize([data["list"]])

df = spark.read.json(rddjson)
#df1 = spark.read.json(rddjson1)

df.write.format("json").mode("overwrite").save("/Users/mro/Documents/Enroute_/Repos/DE101_v2/DE-101-Practices/Practices/session_18_ADF_Transform/data/forecast.json") # we will use this file just as Spark demo
# df1.write.format("json").mode("overwrite").save("/Users/mro/Documents/Enroute_/Repos/DE101_v2/DE-101-Practices/Practices/session_18_ADF_Transform/data/forecast1.json")

# Spark to pandas to csv
df.toPandas().to_csv('/Users/mro/Documents/Enroute_/Repos/DE101_v2/DE-101-Practices/Practices/session_18_ADF_Transform/data/toPandas_forecast.csv', index = False)
# df1.toPandas().to_csv('/Users/mro/Documents/Enroute_/Repos/DE101_v2/DE-101-Practices/Practices/session_18_ADF_Transform/data/toPandas_forecast1.csv', index = False) # we will use this file


# Create a Pandas DataFrame
data_csv = pd.DataFrame([data])
# data_csv1 = pd.DataFrame([data["list"]])

# Pandas to csv
data_csv.to_csv('/Users/mro/Documents/Enroute_/Repos/DE101_v2/DE-101-Practices/Practices/session_18_ADF_Transform/data/pd_forecast.csv', index=False) # we will use this file
# data_csv1.to_csv('/Users/mro/Documents/Enroute_/Repos/DE101_v2/DE-101-Practices/Practices/session_18_ADF_Transform/data/pd_forecast1.csv', index=False)




"""

%%sql
-- Compatibility necessary to use OPENJSON
ALTER DATABASE <DatabaseName> SET COMPATIBILITY_LEVEL = 130


CREATE ?EXTERNAL? TABLE Weather_london_landing (
  clouds varchar(500),
  dt varchar(200),
  dt_txt varchar(200),
  main varchar(500),
  pop varchar(30),
  rain varchar(200),
  sys varchar(200),
  visibility varchar(30),
  weather varchar(500),
  wind varchar(200)
) WITH (
  LOCATION = 'path/to/file.csv',
  DATA_SOURCE = <data_source_name>, -- raw datalake container
  FILE_FORMAT = CSV,
  REJECT_TYPE = VALUE,
  REJECT_VALUE = 0

  -- FORMAT = 'csv',
	-- DATAFILETYPE = 'char',
	FIELDQUOTE = '"',
  FIRSTROW = 2, -- as 1st one is header
  FIELDTERMINATOR = ',',  --CSV field delimiter
  ROWTERMINATOR = '\n'   --Use to shift the control to next row
);



-- create a local table in the sql pool
CREATE TABLE Weather_london (
  cloudiness int,
  dt int,
  dt_txt datetime,
  precip_prob int
  humidity float,
  temp float,
  temp_max float,
  temp_min float,
  visibility float,
  wind_speed float
);







CREATE TABLE json_test_landing (
    cod varchar(20),
    "message" varchar(200),
    cnt varchar(50),
    list varchar(max),
    city varchar (500)
);

DROP TABLE json_test_landing;

CREATE TABLE json_test_final (
  dt int,
  dt_txt datetime,
  cloudiness int,
  precip_prob float,
  humidity float,
  temp float,
  temp_max float,
  temp_min float,
  visibility float,
  wind_speed float
);

DROP TABLE json_test_final;


-- Insert from CSV
BULK INSERT json_test_landing
FROM '/var/opt/mssql/data/pd_forecast.csv'
WITH
(
	FORMAT = 'csv',
	DATAFILETYPE = 'char',
	FIELDQUOTE = '"',
  FIRSTROW = 2, -- as 1st one is header
  FIELDTERMINATOR = ',',  --CSV field delimiter
  ROWTERMINATOR = '\n'   --Use to shift the control to next row
);


-- Transform 1: Change single quote inside list field to doble quotes
UPDATE json_test_landing
SET list = REPLACE(list, char(39),'"')


-- Transform 2 : Extract from JSON, convert data types, insert into final table
DECLARE @json NVARCHAR(MAX);
SELECT @json = list FROM json_test_landing    -- Set list field as json object and insert into
INSERT INTO json_test_final
SELECT *
FROM OPENJSON ( @json )  
WITH (   
    dt  int                 '$.dt',  
    dt_txt  datetime        '$.dt_txt',   
    cloudiness int          '$.clouds.all',
    precip_prob float       '$.pop',
    temp float              '$.main.temp',
    temp_max float          '$.main.temp_max',
    temp_min float          '$.main.temp_min',
    humidity int            '$.main.humidity', 
    visibility float        '$.visibility',
    wind_speed float        '$.wind.speed'
)



-- Set list field as json object and select specific data
DECLARE @json NVARCHAR(MAX);
SELECT @json = list FROM json_test_landing
SELECT *
FROM OPENJSON ( @json )  
WITH (   
    dt  int                 '$.dt',  
    dt_txt  datetime        '$.dt_txt',   
    cloudiness int          '$.clouds.all',
    precip_prob float       '$.pop',
    temp float              '$.main.temp',
    temp_max float          '$.main.temp_max',
    temp_min float          '$.main.temp_min',
    humidity int            '$.main.humidity', 
    visibility float        '$.visibility',
    wind_speed float        '$.wind.speed'
 )





SELECT * FROM json_test_landing;
SELECT * FROM json_test_final;

"""






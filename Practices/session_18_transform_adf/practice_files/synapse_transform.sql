-- CREATE a landing table for the raw data
CREATE TABLE Weather_london_landing
(
    cod varchar(200),
    message varchar(200),
    cnt varchar(50),
    list varchar(MAX),
    city varchar (500)
)
WITH ( CLUSTERED INDEX (cod) 
);


-- COPY the data into the landing table
COPY INTO Weather_london_landing
(
    cod,
    message,
    cnt,
    list,
    city
) 
FROM 'https://<datalake-name>.blob.core.windows.net/<container-name>/raw/pd_forecast.csv'
WITH
(
FIRSTROW=2
);


-- Go to SMSS or Data Studio, open a query from your Synapse connection and run:
/*
SELECT * FROM Weather_london_landing;
*/


-- TRANSFORM 1: Change single quote inside list field to doble quotes in landing table. This is needed for the TRANSFORM 2 that uses OPENJSON function.
UPDATE Weather_london_landing
SET list = REPLACE(list, char(39),'"');


-- SMSS or Data Studio: make sure your data was transformed:
/*
SELECT * FROM Weather_london_landing;
*/


-- Create a local final(cleaned) table in the sql pool
CREATE TABLE Weather_london (
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


-- TRANSFORM 2 : Extract from JSON, convert data types, insert into final table
DECLARE @json NVARCHAR(MAX);
SELECT @json = list FROM Weather_london_landing    -- Set list field as json object and insert into
INSERT INTO Weather_london
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
);



-- SMSS or Data Studio: 
/*
SELECT * FROM Weather_london;
*/


-- Troubleshooting (from SMSS, Data Studio or Synapse script): if you have some problems in the process, you can eliminate the tables an rerun the code
/*
DROP TABLE Weather_london_landing;
DROP TABLE Weather_london;
*/
CREATE TABLE AAPL_landing (
  "Date" varchar(200),
  Low varchar(200),
  "Open" varchar(200),
  Volume varchar(200),
  High varchar(200),
  "Close" varchar(200),
  "Adjusted Close" varchar(200)
);

CREATE TABLE FRED_GDP_landing (
  "Date" varchar(200),
  "Value" varchar(200)
);

CREATE TABLE AAPL (
  "Date" date,
  Low float,
  "Open" float,
  Volume float,
  High float,
  "Close" float,
  "Adjusted Close" float
);

CREATE TABLE FRED_GDP (
  "Date" date,
  "Value" float
);

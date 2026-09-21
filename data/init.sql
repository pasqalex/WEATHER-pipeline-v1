CREATE SCHEMA IF NOT EXISTS raw_data;

CREATE TABLE raw_data.cities (
    city_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    latitude NUMERIC(12, 3),
    longitude NUMERIC(12, 3)
);

CREATE TABLE raw_data.weather_daily (
    weather_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    report_date DATE NOT NULL,
    city_id INTEGER NOT NULL,
    temp_max NUMERIC,
    temp_min NUMERIC,
    precipitation NUMERIC,
    wind_speed NUMERIC,
    FOREIGN KEY (city_id) REFERENCES raw_data.cities(city_id),
    UNIQUE(city_id, report_date)
);
import os
import psycopg
import logging

from dotenv import load_dotenv
from datetime import UTC, datetime
from logging_config import configure_logging

load_dotenv()
configure_logging()

load_logger = logging.getLogger(__name__)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

def loadToDB(data: dict):

    with psycopg.connect(
        dbname=DB_NAME, 
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        connect_timeout=20
        ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rawData (
                    id serial PRIMARY KEY,
                    city text,
                    temperature NUMERIC(4,2),
                    feelsLike NUMERIC(4,2),
                    humidity integer,
                    windSpeed NUMERIC(4,2),
                    windGust NUMERIC(4,2),
                    clouds integer,
                    sunrise bigint,
                    sunset bigint,
                    dt bigint UNIQUE,
                    date timestamptz UNIQUE) 
            """)

            main_data = data.get("main", {})
            wind_data = data.get("wind", {})
            clouds_data = data.get("clouds", {})
            sys_data = data.get("sys", {})

            row = (
                data.get("name"),
                main_data.get("temp"),
                main_data.get("feels_like"),
                main_data.get("humidity"),
                wind_data.get("speed"),
                wind_data.get("gust"),
                clouds_data.get("all"),
                sys_data.get("sunrise"),
                sys_data.get("sunset"),
                data.get("dt"),
                datetime.fromtimestamp(data.get("dt"))
            )

            cur.execute("""
                INSERT INTO rawData (
                    city,
                    temperature,
                    feelsLike, 
                    humidity, 
                    windSpeed, 
                    windGust, 
                    clouds, 
                    sunrise, 
                    sunset,
                    dt, 
                    date_time
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (dt) DO NOTHING
            """, row)

    load_logger.info("Data loaded to data base successfully!")
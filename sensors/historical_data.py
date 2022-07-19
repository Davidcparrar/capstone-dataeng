import configparser
from logs import get_logger
from sensors.sql_queries import query
from io import StringIO  # python3; python2: BytesIO
import boto3
from datetime import datetime
import time

logger = get_logger(__name__)
config = configparser.ConfigParser()
config.read_file(open("config.cfg"))

AWS_KEY = config.get("AWS", "AWS_KEY")
AWS_SECRET = config.get("AWS", "AWS_SECRET")

BUCKET = config.get("STAGING", "BUCKET")
PREFIX_SENSORS = config.get("STAGING", "PREFIX_SENSORS")
URL_DATOS = config.get("STAGING", "URL_DATOS")
DATOS_TOKEN = config.get("STAGING", "DATOS_TOKEN")
DATOS_USER = config.get("STAGING", "DATOS_USER")
DATOS_PWD = config.get("STAGING", "DATOS_PWD")
CLIENT_TEMPERATURE = config.get("STAGING", "CLIENT_TEMPERATURE")
CLIENT_HUMIDITY = config.get("STAGING", "CLIENT_HUMIDITY")

import pandas as pd
from sodapy import Socrata


def save_file(df, name):
    """Store query file in S3 bucket."""
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource(
        "s3",
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )
    s3_resource.Object(BUCKET, f"{PREFIX_SENSORS}/{name}").put(
        Body=csv_buffer.getvalue()
    )


def get_data(
    min_date=None,
    max_date=None,
    client_code=CLIENT_TEMPERATURE,
    query=query,
) -> pd.DataFrame:
    client = Socrata(
        URL_DATOS, DATOS_TOKEN, username=DATOS_USER, password=DATOS_PWD
    )

    # Results returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    query = query.format(min_date=min_date, max_date=max_date)

    results = client.get(client_code, query=query)

    # # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    return results_df


def main():
    start_date = datetime(2012, 6, 12)
    end_date = datetime(2022, 7, 17)
    date_range = pd.date_range(start_date, end_date)

    # Loop through date range, get data and save file
    failed_dates = []
    for date in date_range:
        min_date_str = date.strftime("%Y-%m-%d")
        max_date_str = (date + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        logger.info(f"Getting data for {min_date_str}")
        try:
            df = get_data(min_date_str, max_date_str)
            save_file(df, f"temperature/{min_date_str}.csv")

            df = get_data(
                min_date_str, max_date_str, client_code=CLIENT_HUMIDITY
            )
            save_file(df, f"humidity/{min_date_str}.csv")
        except Exception as e:
            logger.error(f"Error getting data for {min_date_str}")
            logger.error(e)
            failed_dates.append({"failed": min_date_str})

        time.sleep(1)

    if failed_dates:
        df = pd.DataFrame(failed_dates)
        save_file(df, "failed_dates.csv")

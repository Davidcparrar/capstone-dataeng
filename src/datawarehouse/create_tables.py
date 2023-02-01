# from sql_queries import create_table_queries, drop_table_queries
import configparser

import psycopg2

from logs import get_logger
from sensors.sql_queries import query

logger = get_logger(__name__)
config = configparser.ConfigParser()
config.read_file(open("config.cfg"))


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    # connect to default database
    conn = psycopg2.connect(
        f"host={HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute(
        "CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0"
    )

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student"
    )
    cur = conn.cursor()

    return cur, conn

import configparser
from typing import Tuple

import boto3
import numpy as np
import pandas as pd
import xlrd

config = configparser.ConfigParser()
config.read_file(open("../config.cfg"))

AWS_KEY = config.get("AWS", "AWS_KEY")
AWS_SECRET = config.get("AWS", "AWS_SECRET")
BUCKET = config.get("STAGING", "BUCKET")
PREFIX_PRICES = config.get("STAGING", "PREFIX_PRICES")

from logs import get_logger

logger = get_logger(__name__)


def row_col(
    nom_value: str, num_cols: int, num_rows: int, sheet: xlrd.sheet.Sheet
) -> Tuple[int, int]:
    ini_row = None
    ini_col = None
    for row_values in range(0, num_rows):
        for col_values in range(0, num_cols):
            value = sheet.row_values(row_values)[col_values]
            if str(nom_value).lower() in str(value).lower():
                ini_row = row_values
                ini_col = col_values
            if ini_row != None and ini_col != None:
                return ini_col, ini_row

    return None, None


def main(key: str) -> pd.DataFrame:
    s3 = boto3.client(
        "s3", aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET
    )
    obj = s3.get_object(Bucket=BUCKET, Key=f"{PREFIX_PRICES}/{key}")
    workbook = xlrd.open_workbook(file_contents=obj["Body"].read())
    sheet = workbook.sheet_by_name("Boletín diario")

    ini_col, ini_row = row_col("Precio", sheet.ncols, sheet.nrows, sheet)

    names = sheet.row_values(ini_row)
    list_data = []
    # Read Matrix data
    for index_rows in range(ini_row + 1, sheet.nrows):
        data = dict()
        for index_cols in range(ini_col, sheet.ncols):
            data[names[index_cols]] = sheet.cell(index_rows, index_cols).value

        list_data.append(data)

    df = pd.DataFrame(list_data)

    df.replace("", np.nan, inplace=True)
    df.dropna(thresh=df.shape[1] - 2, inplace=True)
    df[df.columns[0]] = df[df.columns[0]].str.replace("*", "", regex=False)
    df[df.columns[0]] = df[df.columns[0]].str.strip()

    df.set_index(df.columns[0], inplace=True)
    keep_cols = [
        col
        for col in df.columns
        if np.any(df[col].str.lower().str.contains("precio"))
    ]
    df = df[keep_cols]

    df = df.replace("n.d.", np.nan)

    df = df.loc[~df.index.isna(), :]

    logger.info(f"Dataframe: {df}")
    return df

import boto3
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import os

# Environment variables
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_FILE = os.environ.get("S3_FILE")

RDS_HOST = os.environ.get("RDS_HOST")
RDS_USER = os.environ.get("RDS_USER")
RDS_PASSWORD = os.environ.get("RDS_PASSWORD")
RDS_DB = os.environ.get("RDS_DB")

GLUE_DATABASE = os.environ.get("GLUE_DATABASE")
GLUE_TABLE = os.environ.get("GLUE_TABLE")


def read_s3():
    print("Reading CSV from S3")

    s3 = boto3.client("s3")

    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_FILE)

    df = pd.read_csv(obj["Body"])

    print(df)

    return df


def create_database_if_not_exists():
    print("Checking database...")

    connection = pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD
    )

    cursor = connection.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {RDS_DB}")

    connection.commit()
    connection.close()

    print("Database ready")


def upload_rds(df):
    print("Uploading data to RDS")

    engine = create_engine(
        f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}/{RDS_DB}"
    )

    df.to_sql("students", engine, if_exists="replace", index=False)

    print("Data inserted into RDS successfully")


def fallback_glue():

    print("RDS failed. Creating Glue table")

    glue = boto3.client("glue")

    glue.create_table(
        DatabaseName=GLUE_DATABASE,
        TableInput={
            "Name": GLUE_TABLE,
            "StorageDescriptor": {
                "Columns": [
                    {"Name": "id", "Type": "int"},
                    {"Name": "name", "Type": "string"},
                    {"Name": "age", "Type": "int"},
                    {"Name": "course", "Type": "string"},
                ],
                "Location": f"s3://{S3_BUCKET}/",
            },
            "TableType": "EXTERNAL_TABLE",
        },
    )

    print("Glue table created")


def main():

    try:

        df = read_s3()

        create_database_if_not_exists()

        upload_rds(df)

    except Exception as e:

        print("Error occurred:", e)

        fallback_glue()


if __name__ == "__main__":
    main()
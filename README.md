# Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application

## Project Overview

This project demonstrates a cloud-based data ingestion pipeline using AWS services and a Dockerized Python application.

The system reads a CSV dataset from an Amazon S3 bucket and loads it into an Amazon RDS MySQL database. If the RDS database is unavailable or the data insertion fails, the system automatically creates a fallback table in AWS Glue Data Catalog referencing the dataset stored in S3.

Amazon Athena can then query the dataset through the Glue metadata.

This project showcases integration between multiple AWS services and containerized data processing.

---

# Architecture

S3 (students.csv)
↓
Dockerized Python Application
↓
Amazon RDS MySQL Database
↓
Fallback → AWS Glue Data Catalog
↓
Query using Amazon Athena

---

# Technologies Used

AWS S3
AWS RDS (MySQL)
AWS Glue Data Catalog
Amazon Athena
Docker
Python
Pandas
Boto3
SQLAlchemy

---

# Project Workflow

1. Upload dataset to Amazon S3
2. Run Docker container with Python ingestion script
3. Python reads CSV file from S3 using boto3
4. Data is converted into a Pandas DataFrame
5. Data is inserted into Amazon RDS MySQL database
6. If RDS insertion fails, AWS Glue table is created as a fallback
7. Data can be queried using Amazon Athena

---

# Project Files

app.py – Python ingestion script
Dockerfile – Container configuration
requirements.txt – Python dependencies
students.csv – Sample dataset

---

# Running the Project

Build the Docker image:

docker build -t data-ingestion-app .

Run the container:

docker run -e AWS_ACCESS_KEY_ID=YOUR_KEY 
-e AWS_SECRET_ACCESS_KEY=YOUR_SECRET 
-e AWS_DEFAULT_REGION=eu-central-1 
-e S3_BUCKET=devops-data-ingestion-bucket 
-e S3_FILE=students.csv 
-e RDS_HOST=your-rds-endpoint 
-e RDS_USER=admin 
-e RDS_PASSWORD=yourpassword 
-e RDS_DB=devopsdb 
-e GLUE_DATABASE=devops_glue_db 
-e GLUE_TABLE=students_table 
data-ingestion-app

---

# Screenshots

## S3 Dataset

![S3 Bucket](screenshots/s3-bucket.png)

## Docker Image Build

![Docker Build](screenshots/docker-build.png)

## Docker Container Run

![Docker Run](screenshots/docker-run.png)

## RDS Data Verification

![RDS Query](screenshots/rds-data.png)

## Glue Table Schema

![Glue Schema](screenshots/glue-schema.png)

## Athena Query

![Athena Query](screenshots/athena-query.png)

---

# Learning Outcomes

Implemented a Dockerized data ingestion pipeline
Integrated AWS S3 with Python using boto3
Loaded structured data into Amazon RDS MySQL
Designed fallback mechanism using AWS Glue
Queried metadata using Amazon Athena

---

# Author

Nikhil Khandare
Cloud / DevOps Engineer

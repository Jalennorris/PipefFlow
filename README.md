##Pipe: PLumbing Service ETL & Analytics Pipeline

##Overview
PipeFlow is a data engineering project that simulates a plumbing service company's job operations pipeline. The project extracts raw CSV data, load it into PostgreSQL, transforms it into cleaned staging tables, validates data quality, logs bad records, and runs SQL analytics queries to answer business questions.

This project was built to demonstrate practical data engineering skills using Python, PostgreSQL,SQL,and ETL design patterns.
---

##Project Goals
-Build an end-to-end ETL pipeline
-Load raw plumbing service data into PostgreSQL
-Transform raw data into cleaned staging tables
-Validate data qualify before analytics
-Log bad records into an error table
-Write SQL analytics queries for business reporting


---

## TEch Stack

-Python
-PostgreSQL
-SQL
-pandas
-psycopg2
-python-dotenv
-Bash/ terminal

## Pipeline Architecture

```text

CSV Files

   ↓

Python Loader

   ↓

PostgreSQL Raw Tables

   ↓

Python Transformation Script

   ↓

PostgreSQL Staging Tables

   ↓

Data Validation + Error Logging

   ↓

SQL Analytics Queries# PipefFlow

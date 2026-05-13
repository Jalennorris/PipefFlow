import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


def load_csv_to_table(csv_path, table_name, columns):
    df = pd.read_csv(csv_path)

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(columns)

    insert_query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING;
    """

    for _, row in df.iterrows():
        values = [None if pd.isna(row[col]) else row[col] for col in columns]
        cursor.execute(insert_query, values)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Loaded {len(df)} rows into {table_name}")


def main():
    load_csv_to_table(
        "data/jobs.csv",
        "raw_jobs",
        [
            "job_id",
            "customer_id",
            "technician_id",
            "job_type",
            "job_status",
            "scheduled_date",
            "completed_date",
            "labor_hours",
            "location_city",
        ],
    )

    load_csv_to_table(
        "data/invoices.csv",
        "raw_invoices",
        [
            "invoice_id",
            "job_id",
            "labor_cost",
            "material_cost",
            "total_amount",
            "paid_status",
        ],
    )

    load_csv_to_table(
        "data/materials.csv",
        "raw_materials",
        [
            "material_id",
            "job_id",
            "material_name",
            "category",
            "quantity",
            "unit_cost",
        ],
    )

    load_csv_to_table(
        "data/technicians.csv",
        "raw_technicians",
        [
            "technician_id",
            "technician_name",
            "specialty",
            "hourly_rate",
        ],
    )


if __name__ == "__main__":
    main()
import os
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


def transform_jobs(cursor):
    cursor.execute("""
        INSERT INTO stg_jobs (
            job_id,
            customer_id,
            technician_id,
            job_type,
            job_status,
            scheduled_date,
            completed_date,
            labor_hours,
            location_city,
            job_duration_days,
            is_completed
        )
        SELECT
            job_id,
            customer_id,
            technician_id,
            LOWER(TRIM(job_type)) AS job_type,
            LOWER(TRIM(job_status)) AS job_status,
            scheduled_date,
            completed_date,
            labor_hours,
            INITCAP(TRIM(location_city)) AS location_city,
            CASE
                WHEN completed_date IS NOT NULL
                THEN completed_date - scheduled_date
                ELSE NULL
            END AS job_duration_days,
            CASE
                WHEN LOWER(TRIM(job_status)) = 'completed'
                THEN TRUE
                ELSE FALSE
            END AS is_completed
        FROM raw_jobs
        ON CONFLICT (job_id) DO NOTHING;
    """)


def transform_invoices(cursor):
    cursor.execute("""
        INSERT INTO stg_invoices (
            invoice_id,
            job_id,
            labor_cost,
            material_cost,
            total_amount,
            paid_status,
            profit_amount
        )
        SELECT
            invoice_id,
            job_id,
            labor_cost,
            material_cost,
            total_amount,
            LOWER(TRIM(paid_status)) AS paid_status,
            total_amount - labor_cost - material_cost AS profit_amount
        FROM raw_invoices
        ON CONFLICT (invoice_id) DO NOTHING;
    """)


def transform_materials(cursor):
    cursor.execute("""
        INSERT INTO stg_materials (
            material_id,
            job_id,
            material_name,
            category,
            quantity,
            unit_cost,
            total_material_cost
        )
        SELECT
            material_id,
            job_id,
            LOWER(TRIM(material_name)) AS material_name,
            LOWER(TRIM(category)) AS category,
            quantity,
            unit_cost,
            quantity * unit_cost AS total_material_cost
        FROM raw_materials
        ON CONFLICT (material_id) DO NOTHING;
    """)


def transform_technicians(cursor):
    cursor.execute("""
        INSERT INTO stg_technicians (
            technician_id,
            technician_name,
            specialty,
            hourly_rate
        )
        SELECT
            technician_id,
            INITCAP(TRIM(technician_name)) AS technician_name,
            LOWER(TRIM(specialty)) AS specialty,
            hourly_rate
        FROM raw_technicians
        ON CONFLICT (technician_id) DO NOTHING;
    """)


def main():
    conn = get_connection()
    cursor = conn.cursor()

    transform_jobs(cursor)
    transform_invoices(cursor)
    transform_materials(cursor)
    transform_technicians(cursor)

    conn.commit()
    cursor.close()
    conn.close()

    print("Transformed raw data into staging tables.")


if __name__ == "__main__":
    main()


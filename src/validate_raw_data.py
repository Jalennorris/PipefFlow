import os
import json
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


def log_error(cursor, pipeline_name, table_name, record_id, error_message, bad_record):
    cursor.execute(
        """
        INSERT INTO etl_error_logs(
            pipeline_name,
            table_name,
            record_id,
            error_message,
            bad_record
        )
        VALUES (%s, %s, %s, %s, %s);
        """,
        (
            pipeline_name,
            table_name,
            str(record_id) if record_id is not None else None,
            error_message,
            json.dumps(bad_record, default=str),
        ),
    )


def validate_jobs(cursor):
    cursor.execute("""
        SELECT
            job_id,
            customer_id,
            technician_id,
            job_type,
            job_status,
            scheduled_date,
            completed_date,
            labor_hours,
            location_city
        FROM raw_jobs;
    """)

    rows = cursor.fetchall()

    for row in rows:
        record = {
            "job_id": row[0],
            "customer_id": row[1],
            "technician_id": row[2],
            "job_type": row[3],
            "job_status": row[4],
            "scheduled_date": row[5],
            "completed_date": row[6],
            "labor_hours": row[7],
            "location_city": row[8],
        }

        job_id = row[0]
        job_status = row[4]
        scheduled_date = row[5]
        completed_date = row[6]
        labor_hours = row[7]

        if job_id is None:
            log_error(cursor, "raw_data_validation", "raw_jobs", job_id, "Missing job_id", record)

        if job_status not in ("completed", "open", "pending", "cancelled"):
            log_error(cursor, "raw_data_validation", "raw_jobs", job_id, "Invalid job_status", record)

        if labor_hours is not None and labor_hours < 0:
            log_error(cursor, "raw_data_validation", "raw_jobs", job_id, "Negative labor_hours", record)

        if completed_date is not None and scheduled_date is not None and completed_date < scheduled_date:
            log_error(cursor, "raw_data_validation", "raw_jobs", job_id, "completed_date is before scheduled_date", record)


def validate_invoices(cursor):
    cursor.execute("""
        SELECT
            invoice_id,
            job_id,
            labor_cost,
            material_cost,
            total_amount,
            paid_status
        FROM raw_invoices;
    """)

    rows = cursor.fetchall()

    for row in rows:
        record = {
            "invoice_id": row[0],
            "job_id": row[1],
            "labor_cost": row[2],
            "material_cost": row[3],
            "total_amount": row[4],
            "paid_status": row[5],
        }

        invoice_id = row[0]
        labor_cost = row[2]
        material_cost = row[3]
        total_amount = row[4]
        paid_status = row[5]

        if invoice_id is None:
            log_error(cursor, "raw_data_validation", "raw_invoices", invoice_id, "Missing invoice_id", record)

        if labor_cost is not None and labor_cost < 0:
            log_error(cursor, "raw_data_validation", "raw_invoices", invoice_id, "Negative labor_cost", record)

        if material_cost is not None and material_cost < 0:
            log_error(cursor, "raw_data_validation", "raw_invoices", invoice_id, "Negative material_cost", record)

        if total_amount is not None and total_amount < 0:
            log_error(cursor, "raw_data_validation", "raw_invoices", invoice_id, "Negative total_amount", record)

        if paid_status not in ("paid", "pending", "overdue", "cancelled"):
            log_error(cursor, "raw_data_validation", "raw_invoices", invoice_id, "Invalid paid_status", record)


def validate_materials(cursor):
    cursor.execute("""
        SELECT
            material_id,
            job_id,
            material_name,
            category,
            quantity,
            unit_cost
        FROM raw_materials;
    """)

    rows = cursor.fetchall()

    for row in rows:
        record = {
            "material_id": row[0],
            "job_id": row[1],
            "material_name": row[2],
            "category": row[3],
            "quantity": row[4],
            "unit_cost": row[5],
        }

        material_id = row[0]
        quantity = row[4]
        unit_cost = row[5]

        if material_id is None:
            log_error(cursor, "raw_data_validation", "raw_materials", material_id, "Missing material_id", record)

        if quantity is not None and quantity <= 0:
            log_error(cursor, "raw_data_validation", "raw_materials", material_id, "Quantity must be greater than 0", record)

        if unit_cost is not None and unit_cost < 0:
            log_error(cursor, "raw_data_validation", "raw_materials", material_id, "Negative unit_cost", record)


def validate_technicians(cursor):
    cursor.execute("""
        SELECT
            technician_id,
            technician_name,
            specialty,
            hourly_rate
        FROM raw_technicians;
    """)

    rows = cursor.fetchall()

    for row in rows:
        record = {
            "technician_id": row[0],
            "technician_name": row[1],
            "specialty": row[2],
            "hourly_rate": row[3],
        }

        technician_id = row[0]
        technician_name = row[1]
        hourly_rate = row[3]

        if technician_id is None:
            log_error(cursor, "raw_data_validation", "raw_technicians", technician_id, "Missing technician_id", record)

        if technician_name is None or str(technician_name).strip() == "":
            log_error(cursor, "raw_data_validation", "raw_technicians", technician_id, "Missing technician_name", record)

        if hourly_rate is not None and hourly_rate <= 0:
            log_error(cursor, "raw_data_validation", "raw_technicians", technician_id, "Hourly rate must be greater than 0", record)


def main():
    conn = get_connection()
    cursor = conn.cursor()

    validate_jobs(cursor)
    validate_invoices(cursor)
    validate_materials(cursor)
    validate_technicians(cursor)

    conn.commit()
    cursor.close()
    conn.close()

    print("Validation complete. Check etl_error_log for issues.")


if __name__ == "__main__":
    main()
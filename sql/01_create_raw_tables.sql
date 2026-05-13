CREATE TABLE IF NOT EXISTS raw_jobs (
    job_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    technician_id INTEGER,
    job_type TEXT,
    job_status TEXT,
    scheduled_date DATE,
    completed_date DATE,
    labor_hours NUMERIC,
    location_city TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_invoices (
    invoice_id INTEGER PRIMARY KEY,
    job_id INTEGER,
    labor_cost NUMERIC,
    material_cost NUMERIC,
    total_amount NUMERIC,
    paid_status TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_materials (
    material_id INTEGER PRIMARY KEY,
    job_id INTEGER,
    material_name TEXT,
    category TEXT,
    quantity INTEGER,
    unit_cost NUMERIC,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_technicians (
    technician_id INTEGER PRIMARY KEY,
    technician_name TEXT,
    specialty TEXT,
    hourly_rate NUMERIC,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
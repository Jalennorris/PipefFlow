CREATE TABLE IF NOT EXISTS stg_jobs (
    job_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    technician_id INTEGER NOT NULL,
    job_type TEXT NOT NULL,
    job_status TEXT NOT NULL,
    scheduled_date DATE NOT NULL,
    completed_date DATE,
    labor_hours NUMERIC,
    location_city TEXT NOT NULL,
    job_duration_days INTEGER,
    is_completed BOOLEAN,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_invoices (
    invoice_id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL,
    labor_cost NUMERIC NOT NULL,
    material_cost NUMERIC NOT NULL,
    total_amount NUMERIC NOT NULL,
    paid_status TEXT NOT NULL,
    profit_amount NUMERIC,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_materials (
    material_id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL,
    material_name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_cost NUMERIC NOT NULL,
    total_material_cost NUMERIC,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_technicians (
    technician_id INTEGER PRIMARY KEY,
    technician_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    hourly_rate NUMERIC NOT NULL,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
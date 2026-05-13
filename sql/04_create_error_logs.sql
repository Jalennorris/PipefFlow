CREATE TABLE IF NOT EXISTS etl_error_logs(
    error_id SERIAL PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_id TEXT,
    error_message TEXT NOT NULL,
    bad_record JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



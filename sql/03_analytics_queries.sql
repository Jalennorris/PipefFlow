-- View All Completed Jobs

SELECT 
    job_id,
    job_type,
    job_status,
    location_city,
    scheduled_date,
    completed_date,
    labor_hours,
FROM stg_jobs
WHERE is_completed = "TRUE";


--Revenue by Job Type

SELECT
    j.job_type,
    SUM(i.total_amount) AS total_revenue
FROM stg_jobs j
JOIN stg_invoices i
    ON j.job_id = = i.job_id
GROUP BY j.job_type
ORDER BY total_revenue DESC;


--Profit by Job Type
SELECT 
    j.job_type,
    SUM(i.profit_amount) AS total_profit
FROM stg_jobs j
JOIN stg_invoices i
    ON j.job_id = i.job_id;
GROUP BY j.job_type
ORDER BY total_profit DESC;

--Technician Productivity
SELECT 
    t.technician_name,
    t.specialty,
    COUNT(j.job_id) AS completed_jobs,
    SUM(j.labor_hours) AS total_labor_hours

FROM stg_technicians t
JOIN stg_jobs j
    ON t.technician_id = j.technician_id
WHERE j.is_completed = "TRUE"
GROUP BY t.technician_name, t.specialty
ORDER BY completed_jobs DESC;

--Average Job Duration by Job TYpe
SELECT
    job_type,
    AVG(job_duration_days) AS avg_duration_days
FROM stg_jobs
WHERE is_completed = "TRUE"
GROUP BY job_type
ORDER BY avg_duration_days DESC;

--Revenue by location

SELECT 
    j.location_city,
    SUM(i.total_amount) AS total_revenue
FROM stg_jobs j
JOIN stg_invoices i
    ON j.job_id = i.job_id
GROUP BY j.location_city
ORDER BY total_revenue DESC;


-- Material Cost by category

SELECT
    category,
    SUM(total_material_cost) AS total_material_cost
FROM stg_materials
GROUP BY category
ORDER BY total_material_cost DESC;


-- Highest Revenue Jobs

SELECT
    j.job_id,
    j.job_type,
    j.location_city,
    i.total_amount
FROM stg_jobs j
JOIN stg_invoices i
    ON j.job_id = i.job_id
ORDER BY i.total_amount DESC;


--Low Profit Jobs

SELECT
    j.job_id,
    j.job_type,
    j.location_city,
    i.total_amount,
    i.labor_cost,
    i.material_cost,
    i.profit_amount
FROM stg_jobs j
JOIN stg_invoices i
    ON j.job_id = i.job_id
WHERE i.profit_amount <= 0;
ORDER BY i.profit_amount ASC;

-- Paid vs Pending Invoices
SELECT
    paid_status,
    COUNT((*)) AS invoice_count,
    SUM(total_amount) AS total_amount
FROM stg_invoices
GROUP BY paid_status
ORDER BY total_amount DESC;
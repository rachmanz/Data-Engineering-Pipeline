-- Membuat database jika belum ada (antisipasi cadangan)
SELECT 'CREATE DATABASE de_project' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'de_project')\gexec

-- Pindah ke database de_project
\c de_project;

-- Membuat skema khusus jika diperlukan di masa depan (opsional)
CREATE SCHEMA IF NOT EXISTS staging;

-- Set timezone agar sinkron dengan waktu Airflow (UTC)
SET timezone = 'UTC';
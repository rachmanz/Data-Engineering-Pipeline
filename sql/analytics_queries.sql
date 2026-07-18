-- =====================================================================
-- POST-INGESTION ANALYTICS & DATA QUALITY CHECKS FOR USERS_ETL
-- =====================================================================

-- Mengintip 10 data pertama untuk validasi kolom snake_case
SELECT id, first_name, last_name, email, university, gender 
FROM users_etl 
LIMIT 10;

-- Analisis Demografi: Menghitung jumlah user berdasarkan Universitas (Top 5)
SELECT 
    university, 
    COUNT(*) as total_students
FROM users_etl
GROUP BY university
ORDER BY total_students DESC
LIMIT 5;

-- Data Quality Check: Memastikan tidak ada email atau ID yang duplikat
SELECT 
    email, 
    COUNT(*) as duplicate_count
FROM users_etl
GROUP BY email
HAVING COUNT(*) > 1;

-- Audit Data: Cek apakah ada kolom krusial yang bernilai NULL/Kosong
SELECT 
    COUNT(*) FILTER (WHERE first_name IS NULL) as missing_first_name,
    COUNT(*) FILTER (WHERE email IS NULL) as missing_email,
    COUNT(*) FILTER (WHERE university IS NULL) as missing_university
FROM users_etl;
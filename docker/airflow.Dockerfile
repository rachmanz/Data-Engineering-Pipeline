FROM apache/airflow:2.8.1-python3.10

# Salin file requirements jika ada, atau langsung install dependency utama
RUN pip install --no-cache-dir \
    requests \
    pandas \
    sqlalchemy \
    psycopg2-binary
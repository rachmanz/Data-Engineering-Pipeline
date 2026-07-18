from datetime import datetime, timedelta
import sys
import os

# Trik penting: Menambahkan folder 'src' ke system path Python di dalam container Airflow
sys.path.append(os.path.join(os.path.dirname(__file__), '../config'))

from airflow import DAG
from airflow.operators.python import PythonOperator

# Impor fungsi-fungsi dari folder src
from src.extract import extract_user
from src.transform import transform_user
from src.load import load_user

# Konfigurasi Database (Host diarahkan ke nama service docker 'postgres')
DB_CONFIG = {
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': 'postgres', 
    'port': '5432',
    'name': os.getenv('POSTGRES_DB', 'de_project')
}

# Wrapper fungsi agar Airflow bisa menjembatani data via XCom (return value)
def extract_task_callable():
    return extract_user()

def transform_task_callable(ti):
    raw_df = ti.xcom_pull(task_ids='extract_data_task')
    return transform_user(raw_df)

def load_task_callable(ti):
    clean_df = ti.xcom_pull(task_ids='transform_data_task')
    load_user(clean_df, DB_CONFIG)

# Konfigurasi bawaan DAG
default_args = {
    'owner': 'data_engineering_team',
    'start_date': datetime(2026, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='enterprise_etl_users_pipeline',
    default_args=default_args,
    schedule_interval='@daily', # Berjalan otomatis sekali setiap hari
    catchup=False,
    tags=['production', 'etl', 'dummyjson']
) as dag:

    task_extract = PythonOperator(
        task_id='extract_data_task',
        python_callable=extract_task_callable
    )

    task_transform = PythonOperator(
        task_id='transform_data_task',
        python_callable=transform_task_callable
    )

    task_load = PythonOperator(
        task_id='load_data_task',
        python_callable=load_task_callable
    )

    # Mengatur alur eksekusi (Workflow Dependency)
    task_extract >> task_transform >> task_load
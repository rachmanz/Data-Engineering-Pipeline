from sqlalchemy import create_engine
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_user(dataframe: pd.DataFrame, db_config: dict):
    """Mengirim DataFrame yang sudah bersih ke container PostgreSQL."""
    try:
        # Menyusun URL Koneksi Database dari parameter db_config yang dikirim oleh Airflow
        DATABASE_URL = (
            f"postgresql://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['name']}"
        )

        # Inisialisasi Engine SQLAlchemy
        engine = create_engine(DATABASE_URL)    
        
        # Mengirim data ke tabel 'users_etl'
        dataframe.to_sql(
            name='users_etl', 
            con=engine, 
            if_exists='replace', 
            index=False
        )
        logging.info(f"[LOAD] Sukses mendorong {len(dataframe)} baris data ke PostgreSQL Container! 🚀")
        
    except Exception as e:
        logging.error(f"[LOAD GAGAL] Gagal memasukkan data ke database: {e}")
        raise e
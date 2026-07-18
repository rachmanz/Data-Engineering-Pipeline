import pandas as pd               # Fungsi filter kolom data apa saja yang ingin diambil
import re                         # Regular Expression (Pengubahan nama pada kolom)
import logging                    # Membuat log pada proses transformasi (biasanya ini banyak error)

#  Basic Logging Format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#  Data Processor (Cek Validitas Dat)
class DataProcessor:
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input 'data' harus berupa Pandas DataFrame!")
        self.data = data.copy()

    def check_missing_values(self):
        try:
            if self.data.isnull().values.any():
                total_missing = self.data.isnull().sum().sum()
                logging.info(f"[Warning] Ditemukan {total_missing} missing value pada data.")
            else:
                logging.info("Data tidak ada baris kosong ✅")
        except Exception as e:
            logging.error(f"[Gagal] Proses pengecekan missing value bermasalah: {e}")

# Filter Data (Tranformasi Data)
class DataFilter(DataProcessor):
    def __init__(self, data: pd.DataFrame, filter_columns: list):
        super().__init__(data)
        if not all(isinstance(col, str) for col in filter_columns):
            raise TypeError("Semua item di dalam list 'filter_columns' harus berupa string!")
        self.filter_columns = filter_columns

    def _to_snake_case(self, name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def filter_columns_data(self):
        try:
            self.data = self.data[self.filter_columns]
        except KeyError as e:
            raise KeyError(f"Ada kolom dari list filter yang tidak ditemukan di DataFrame: {e}")

    def rename_columns(self):
        rename_mapping = {col: self._to_snake_case(col) for col in self.filter_columns}
        self.data = self.data.rename(columns=rename_mapping)

    def remove_duplicate(self):
        try:
            initial_rows = len(self.data)
            self.data = self.data.drop_duplicates()
            final_rows = len(self.data)
            if final_rows < initial_rows:
                logging.info(f"[Info] Berhasil menghapus {initial_rows - final_rows} baris duplikat.")
            else:
                logging.info("Data tidak ada baris duplikat ✅")
        except Exception as e:
            logging.error(f"[Gagal] Proses pengecekan duplikat bermasalah: {e}")

    def process(self):
        self.filter_columns_data()
        self.rename_columns()
        self.remove_duplicate()
        super().check_missing_values()
        return self.data

# Membungkus proses ke dalam fungsi agar bisa dipanggil Airflow
def transform_user(dataframe):
    filter_data = [
        'id', 'firstName', 'lastName', 'age', 'gender', 'email', 'phone',
        'username', 'birthDate', 'bloodGroup', 'height', 'weight', 'university', 'role'
    ]
    cleaner = DataFilter(dataframe, filter_data)
    return cleaner.process()
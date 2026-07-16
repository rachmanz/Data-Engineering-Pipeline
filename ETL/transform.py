from extract import extract_user  # Data dari extract oper ke transform 
import pandas as pd               # Fungsi filter kolom data apa saja yang ingin diambil
import re                         # Regular Expression (Pengubahan nama pada kolom)
import logging                    # Membuat log pada proses transformasi (biasanya ini banyak error)

# Setup Logger Report Format 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Pemrosesan Data
class DataProcessor:
    """Class Induk untuk menangani validasi dasar DataFrame."""
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input 'data' harus berupa Pandas DataFrame!")
        self.data = data.copy()

    def check_missing_values(self):
        """Mengecek keberadaan missing value."""
        try:
            if self.data.isnull().values.any():
                total_missing = self.data.isnull().sum().sum()
                logging.info(f"[Warning] Ditemukan {total_missing} missing value pada data.")
            else:
                logging.info("Data tidak ada baris kosong ✅")
        except Exception as e:
            logging.info(f"[Gagal] Proses pengecekan missing value bermasalah: {e}")

# Filter Data
class DataFilter(DataProcessor):
    """Class dengan fungsi filter kolom, rename, dan pembersihan data"""
    
    def __init__(self, data: pd.DataFrame, filter_columns: list):
        # Memanggil __init__ milik DataProcessor (Induk) menggunakan super()
        super().__init__(data)
        
        # Validasi list filter harus string
        if not all(isinstance(col, str) for col in filter_columns):
            raise TypeError("Semua item di dalam list 'filter_columns' harus berupa string!")
        
        self.filter_columns = filter_columns

    def _to_snake_case(self, name: str) -> str:
        """Fungsi internal untuk mengubah camelCase menjadi snake_case."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def filter_columns_data(self):
        """  Filter Kolom """
        try:
            self.data = self.data[self.filter_columns]
        except KeyError as e:
            raise KeyError(f"Ada kolom dari list filter yang tidak ditemukan di DataFrame: {e}")

    def rename_columns(self):
        """ Membuat nama kolom menjadi format snake_case """
        rename_mapping = {col: self._to_snake_case(col) for col in self.filter_columns}
        self.data = self.data.rename(columns=rename_mapping)

    def remove_duplicate(self):
        """ Menghapus duplikat """
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

    def check_missing(self):
        """ Pengecekan missing value """
        # Memanggil fungsi check_missing_values dari Class Induk menggunakan super(): inheritance
        super().check_missing_values()

    def process(self):
        """Menjalankan seluruh alur pipeline pembersihan data secara berurutan."""
        self.filter_columns_data()    #  Langkah 1 (Filter Kolom Data)
        self.rename_columns()         #  Langkah 2 (Rename dengan format)
        self.remove_duplicate()       #  Langkah 3 (Membuang Duplikat Data)
        self.check_missing()          #  Langkah 4 (Cek Missing Value)
        
        return self.data              #  Mengembalikan data dalam bentuk jadi

# Program running....
if __name__ == "__main__":
    # Filter kolom target
    filter_data = [
        'id',
        'firstName', 
        'lastName', 
        'age', 
        'gender', 
        'email', 
        'phone',
        'username', 
        'birthDate', 
        'bloodGroup',
        'height', 
        'weight', 
        'university', 
        'role'
    ]
    
    # Jalankan Progam Transform 
    cleaner = DataFilter(data_extract, filter_data) # Masukan dalam proses filter
    transform_process = cleaner.process()           # Proses datanya
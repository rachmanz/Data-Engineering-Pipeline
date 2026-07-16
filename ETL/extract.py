# Library 
import requests
import pandas as pd

# Fungsi untuk extract data request (menjadi sebuah dataframe)
def extract_user():
    URL = "https://dummyjson.com/users" # URL Endpoint yang digunakan
    response = requests.get(URL)        # Mengirimkan data ke Endpoint URL
    data = response.json()              # Mendapatkan data JSON format
    dataframe = pd.DataFrame(user)      # Ubah data menjadi dataframe
    return dataframe                    # Mengembalikan bentuk dari dataframe


# Program running....
if __name__ == "__main__":
    # USE THIS IF YOU NOT IMPLEMENT AIRFLOW
    # URL = "https://dummyjson.com/users" # URL Dummy untuk mendapatkan data
    # response = requests.get(URL)        # Buat Bridge Connection mendapatkan data
    # data = response.json()              # Response JSON (Raw Data)

    # Jalankan Fungsional Extract
    data_extract = extract_user() # Dilanjutkan pada transform

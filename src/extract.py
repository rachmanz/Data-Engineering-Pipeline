# Library 
import requests
import pandas as pd
import logging


# Fungsi untuk extract data request (menjadi sebuah dataframe)
def extract_user():
    URL = "https://dummyjson.com/users" # URL Endpoints
    response = requests.get(URL)        # Response URL (Send)
    data = response.json()              # Dapatkan response dalam bentuk JSON
    
    # DummyJSON mengembalikan dict dengan key 'users' yang berisi list
    if 'users' in data:
        dataframe = pd.DataFrame(data['users'])
        logging.info(f"Berhasil extract {len(dataframe)} baris data dari API.")
        return dataframe
    else:
        raise KeyError("Key 'users' tidak ditemukan dalam response API!")
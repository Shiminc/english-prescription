import pandas as pd
import requests, sys, os, io
from zipfile import ZipFile
import io
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

path_sep = 'https://files.digital.nhs.uk/2F/09F237/gp-reg-pat-prac-all.zip'
path_aug = 'https://files.digital.nhs.uk/45/E255E0/gp-reg-pat-prac-all.zip'
path_jul = 'https://files.digital.nhs.uk/0C/C6EF77/gp-reg-pat-prac-all.zip'
path_jun = 'https://files.digital.nhs.uk/15/4E45A6/gp-reg-pat-prac-all.zip'
path_may = 'https://files.digital.nhs.uk/4F/64EF9E/gp-reg-pat-prac-all.zip'
path_apr = 'https://files.digital.nhs.uk/0D/5048F1/gp-reg-pat-prac-all.csv'

    # if path.endswith('.csv'):

def get_csv(path):
    response = requests.get(path, timeout=30)
    response.raise_for_status()
    df = pd.read_csv(path)
    df = process_data(df)
    return df

def get_zipped_csv(path):
    response = requests.get(path, timeout=30)
    response.raise_for_status()

    # Extract and read CSV
        
    with ZipFile(io.BytesIO(response.content)) as myzip:
        # csv_files = [f for f in myzip.namelist() if f.endswith('.csv')]
        csv_file = myzip.namelist()[0]
        with myzip.open(csv_file) as f:
            df = pd.read_csv(f)
    return df

def process_data(df):
    df = df[['EXTRACT_DATE','CODE','NUMBER_OF_PATIENTS']]
    df.columns = ['year_month','practice_code','patients_num']
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m-%d')

    return df
def main():
    data_apr = get_csv(path_apr)
    data_sep = get_zipped_csv(path_sep)
    print('finish')

# main()
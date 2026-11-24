import glob, os, sys, re
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

path = os.getcwd() + './data/antidepressant_prescribed'
path = './data/antidepressant_prescribed'

def collate_all_antidepressant_data():
    files = glob.glob(path +'/*.csv')
    master_df = pd.DataFrame()
    for file in files:
        yearmonth = re.search(r'(\d{6})',file)
        data = pd.read_csv(file)
        data['yearmonth']=yearmonth.group()
        master_df = pd.concat([master_df,data])

    # drop the first column which is the unnamed index from the csv
    master_df = master_df.iloc[:,1:]

    return master_df

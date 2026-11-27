import sys, os
import pandas as pd
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import collate_all_antidepressant_data, all_drugs
from utils_patient import get_csv

path_apr = 'https://files.digital.nhs.uk/0D/5048F1/gp-reg-pat-prac-all.csv'



def main():
    data_antidepressant = collate_all_antidepressant_data()
    # data_all_drugs = all_drugs()
    patients_data = get_csv(path_apr)
    print('finish')

main()
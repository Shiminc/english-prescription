import sys, os
import pandas as pd
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import collate_all_antidepressant_data, all_drugs




def main():
    data_antidepressant = collate_all_antidepressant_data()
    data_all_drugs = all_drugs()
    
    print('finish')

main()
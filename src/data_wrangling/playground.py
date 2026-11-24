import sys, os
import pandas as pd
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import collate_all_antidepressant_data



def main():
    data = collate_all_antidepressant_data()
    print('finish')

main()
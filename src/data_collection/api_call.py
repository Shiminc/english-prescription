import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import requests
import warnings
warnings.simplefilter("ignore", category=UserWarning)


base_endpoint = 'https://opendata.nhsbsa.net/api/3/action/'
action_method = 'datastore_search_sql?'  # SQL action method
resource_name = 'EPD_SNOMED_202609' # For EPD resources are named EPD_YYYYMM


antidepressant_path = './data/snomed_antidepressant.csv'


def read_antidepressant():
    data = pd.read_csv(os.getcwd()+ antidepressant_path)
    data['Antidepressant'] = data['Antidepressant'].str.strip()
    # string_literal = '\',\''.join(list(data['Antidepressant']))
    # string_literal = '\'' + string_literal + '\''
    # return string_literal
    return list(data['Antidepressant'])

def query_api(drug):
    query = "SELECT * " \
            f"FROM `{resource_name}` " \
            f"WHERE bnf_chemical_substance = '{drug}'"

    api_call = f"{base_endpoint}" \
               f"{action_method}" \
               "resource_id=" \
                    f"{resource_name}" \
               "&" \
               "sql=" \
                    f"{query}"
    response = requests.get(api_call).json()
    if response['success']:
        df  = pd.json_normalize(response['result']['result']['records'])
    return df

def collect_data(drug_list):
    for drug in drug_list[:10]:
        df = query_api(drug)
        if drug == 'Agomelatine':
            master_df = df
        else:
            master_df = pd.concat([master_df,df])
    return master_df

def main():
    drug_list = read_antidepressant()
    data = collect_data(drug_list)
    

    
    print('finish')

main()

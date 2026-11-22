import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import requests
import warnings
warnings.simplefilter("ignore", category=UserWarning)


base_endpoint = 'https://opendata.nhsbsa.net/api/3/action/'
action_method = 'datastore_search_sql?'  # SQL action method
resource_name = 'EPD_SNOMED_202604' # For EPD resources are named EPD_YYYYMM

resource_list = ['EPD_SNOMED_202604', 'EPD_SNOMED_202605','EPD_SNOMED_202606','EPD_SNOMED_202607','EPD_SNOMED_202608','EPD_SNOMED_202609']
antidepressant_path = './data/snomed_antidepressant.csv'


def read_antidepressant():
    data = pd.read_csv(os.getcwd()+ antidepressant_path)
    data['Antidepressant'] = data['Antidepressant'].str.strip()
    # string_literal = '\',\''.join(list(data['Antidepressant']))
    # string_literal = '\'' + string_literal + '\''
    # return string_literal
    return list(data['Antidepressant'])

def query_gp():
    query = "SELECT DISTINCT practice_name,practice_code,address_1, address_2, address_3, address_4,postcode " \
            f"FROM `{resource_name}` " \

    api_call = f"{base_endpoint}" \
               f"{action_method}" \
               "resource_id=" \
                    f"{resource_name}" \
               "&" \
               "sql=" \
                    f"{query}"
    response = requests.get(api_call).json()
    if response['success']:
        print('success')

        df  = pd.json_normalize(response['result']['result']['records'])
    else:
        print('failed')
        df = pd.DataFrame()
    return df

def get_overall_drug_api(resource):
    query = "SELECT year_month, practice_name,practice_code,icb_name,pco_name, SUM(ITEMS) AS TOTAL_by_item " \
            f"FROM `{resource}` " \
            f"GROUP BY year_month, practice_name,practice_code,icb_name,pco_name"

    api_call = f"{base_endpoint}" \
               f"{action_method}" \
               "resource_id=" \
                    f"{resource}" \
               "&" \
               "sql=" \
                    f"{query}"
    response = requests.get(api_call).json()
    if response['success']:
        print('success',all)

        df  = pd.json_normalize(response['result']['result']['records'])
    else:
        print('failed',all)
        df = pd.DataFrame()
    return df

def complex_query_api(drug):
    query = "SELECT bnf_chemical_substance,practice_name,practice_code,icb_name,pco_name, SUM(ITEMS) AS TOTAL_by_item " \
            f"FROM `{resource_name}` " \
            f"WHERE bnf_chemical_substance = '{drug}'" \
            f"GROUP BY bnf_chemical_substance,practice_name,practice_code,icb_name,pco_name"

    api_call = f"{base_endpoint}" \
               f"{action_method}" \
               "resource_id=" \
                    f"{resource_name}" \
               "&" \
               "sql=" \
                    f"{query}"
    response = requests.get(api_call).json()
    if response['success']:
        print('success',drug)

        df  = pd.json_normalize(response['result']['result']['records'])
    else:
        print('failed',drug)
        df = pd.DataFrame()
    return df

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
    for drug in drug_list:
        df = complex_query_api(drug)
        if drug == 'Agomelatine':
            master_df = df
        else:
            master_df = pd.concat([master_df,df])
    return master_df

def collect_overall_data(resource_list):
    for resource in resource_list:
        df = get_overall_drug_api(resource)
        if resource == 'EPD_SNOMED_202604':
            master_df = df
        else:
            master_df = pd.concat([master_df,df])
    return master_df


def main():
    # drug_list = read_antidepressant()
    # data = collect_data(drug_list)
    # data = complex_query_api('Citalopram hydrobromide')
    # data = query_gp()
    data = collect_overall_data(resource_list)
    print('finish')

main()

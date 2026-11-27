import sys, os
import pandas as pd
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import collate_all_antidepressant_data, all_drugs,set_up_altair_browser
import altair as alt

def create_bar(data):
    chart = alt.Chart(data).mark_bar().encode(
        x = alt.X('icb_name').sort('-y').axis(None),
        y = alt.Y('antidepressant_prop'),
        row = alt.Row('year_month'),
        color = alt.Color('icb_name'),
        tooltip = alt.Tooltip('icb_name')
    )
    return chart

def merge_with_calculation(icb_antidepressant,icb_all_drugs):
    data = pd.merge(icb_antidepressant,icb_all_drugs, on = ['icb_name','year_month'])
    data['antidepressant_prop'] = data['antidepressant_total']/data['all_drugs_total']
    return data

def collect_icb_all_drugs(data_all_drugs):
    data = data_all_drugs.groupby(by=['icb_name','icb_code','year_month'])['all_drugs_total'].sum()    
    data = data.reset_index()
    data['year_month'] = pd.to_datetime(data['year_month'], format='%Y-%m')

    return data

def collect_icb_antidepressant(data_antidepressant):
    data = data_antidepressant.groupby(by=['icb_name','year_month'])['TOTAL_by_item'].sum()    
    data = data.reset_index()
    data = data.rename(columns={'TOTAL_by_item':'antidepressant_total'})
    data['year_month'] = pd.to_datetime(data['year_month'], format='%Y%m')

    return data

def main():
    set_up_altair_browser()
    data_antidepressant = collate_all_antidepressant_data()
    icb_antidepressant = collect_icb_antidepressant(data_antidepressant)
    data_all_drugs = all_drugs()
    icb_all_drugs = collect_icb_all_drugs(data_all_drugs)
    data = merge_with_calculation(icb_antidepressant,icb_all_drugs)
    create_bar(data).show()
    print('finish')

main()
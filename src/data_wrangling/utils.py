import glob, os, sys, re
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import altair as alt

path_antidepressant = './data/antidepressant_prescribed'
path_all_drugs = './data/all_drugs_prescribed_by_practices_202604_09.csv'
path_patients = './data/gp-reg-pat-prac-sing-age-region.csv'

def all_drugs():
    data = pd.read_csv(path_all_drugs)
    # drop the first column which is the unnamed index from the csv
    data = data.iloc[:,1:]
    data.rename(columns={'TOTAL_by_item':'all_drugs_total'},inplace=True)
    return data
    
def collate_all_antidepressant_data():
    files = glob.glob(path_antidepressant +'/*.csv')
    master_df = pd.DataFrame()
    for file in files:
        yearmonth = re.search(r'(\d{6})',file)
        data = pd.read_csv(file)
        data['year_month']=yearmonth.group()
        master_df = pd.concat([master_df,data])

    master_df ['year_month'] = pd.to_datetime(master_df['year_month'], format='%Y%m')

    # drop the first column which is the unnamed index from the csv
    master_df = master_df.iloc[:,1:]
    master_df = remove_drugs(master_df)
    master_df = combine_drugs(master_df)
    return master_df

def remove_drugs(df):
    # sulpiride mainly antipsychotic, Bupropion hydrochloride for smoking cessation
    # also not on Mind list https://www.mind.org.uk/information-support/drugs-and-treatments/medication/antidepressants/comparing-antidepressants/
    to_remove = ['Sulpiride','Bupropion hydrochloride']
    df = df[~df['bnf_chemical_substance'].isin(to_remove)]
    return df

def combine_drugs(df):
    to_combine = ['Citalopram hydrobromide','Citalopram hydrochloride','Doxepin','Doxepin hydrochloride']
    master_df = df[~df['bnf_chemical_substance'].isin(to_combine)]

    citalopram_df = df[df['bnf_chemical_substance'].isin(['Citalopram hydrobromide','Citalopram hydrochloride'])]
    citalopram_df['bnf_chemical_substance']='Citalopram'
    citalopram_df = citalopram_df.groupby(by=['bnf_chemical_substance', 'practice_name', 'practice_code', 'icb_name','pco_name', 'year_month'])['TOTAL_by_item'].sum()
    citalopram_df = pd.DataFrame(citalopram_df.reset_index())

    doxepin_df = df[df['bnf_chemical_substance'].isin(['Doxepin','Doxepin hydrochloride'])]
    doxepin_df['bnf_chemical_substance']='Doxepin'
    doxepin_df = doxepin_df.groupby(by=['bnf_chemical_substance', 'practice_name', 'practice_code', 'icb_name','pco_name', 'year_month'])['TOTAL_by_item'].sum()
    doxepin_df = pd.DataFrame(doxepin_df.reset_index())

    master_df = pd.concat([master_df, citalopram_df, doxepin_df])
    return master_df.reset_index()

def set_up_altair_browser():
    alt.renderers.enable('browser')
    alt.renderers.set_embed_options(loader={"target": "_blank"})
    #alt.renderers.enable('mimetype') # offline renderer
    alt.data_transformers.disable_max_rows()

def set_up_altair_jupyter():
    alt.renderers.enable('jupyter') # offline renderer
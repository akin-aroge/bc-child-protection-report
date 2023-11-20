import pandas as pd
from pathlib import Path
from src import utils
from src import constants as C
import numpy as np

proj_root_dir = utils.get_proj_root()

data_dir = proj_root_dir.joinpath('data/raw')




def remove_comma(df:pd.DataFrame):
    data = df.copy()
    for col in df.columns:
        try:
            data[col] = data[col].str.replace(',', '')
        except (TypeError, AttributeError):
            pass

    return data

def parse_numeric_cols(df:pd.DataFrame, cols:list):
    data = df.copy()
    data = remove_comma(data)
    for col in cols:
        try:
            data[col] = pd.to_numeric(data[col])
        except TypeError:
            pass
    
    return data

def remove_superscript(df:pd.DataFrame):
    data = df.copy()
    cols = df.columns
    for col in cols:
        df[col]= data[col].apply(lambda x: x[:-1] if ends_with_superscript(x) else x)

    return df

def ends_with_superscript(str_:str):
    str_ints = list(map(str, range(10)))
    try:
        has_superscript =   str_[-1] in str_ints and str_[-2] not in str_ints
    except (TypeError, IndexError):
        has_superscript = False
    return has_superscript
        

def sanitize_data(df:pd.DataFrame, numerical_cols:list, drop_last_row=False, ):
    data = df.copy()
    data.replace({'*':np.NaN, '-':0}, inplace=True)
    data = remove_superscript(data)
    data = parse_numeric_cols(data, cols=numerical_cols)

    if drop_last_row:
        data = data.iloc[:-1, :]

    return data

def get_reports_data():
    
    new_protection_reports = pd.read_csv(data_dir.joinpath('child_protection_reports/new_protection_reports.csv'))
    reports_by_caller = pd.read_csv(data_dir.joinpath('child_protection_reports/protection_reports_by_caller.csv'))
    report_with_safety_concerns = pd.read_csv(data_dir.joinpath('child_protection_reports/protection_report_with_safety_concerns.csv'))

    numerical_cols_reports = new_protection_reports.columns[1:]
    numerical_cols_caller = ['Protection Reports']

    new_protection_reports =  sanitize_data(new_protection_reports, numerical_cols=numerical_cols_reports, drop_last_row=False)
    report_with_safety_concerns = sanitize_data(report_with_safety_concerns, numerical_cols=numerical_cols_reports, drop_last_row=False)

    sda_col_name = 'Service Delivery Area'
    suffix_reports = C.MERGE_SUFFIXES['suffix_reports']
    suffix_reports_with_concern = C.MERGE_SUFFIXES['suffix_reports_with_concern']
    temp_df = new_protection_reports.merge(right=report_with_safety_concerns, 
                                        on=sda_col_name, suffixes=(suffix_reports, suffix_reports_with_concern) )

    return temp_df

def get_care_data():
    care_admissions = pd.read_csv(data_dir.joinpath('services_needing_protection/admissions_into_care.csv'))
    ooc_agreements = pd.read_csv(data_dir.joinpath('services_needing_protection/new_ooc_agreements.csv'))
    numerical_cols_admissions = care_admissions.columns[1:]
    care_admissions =  sanitize_data(care_admissions, numerical_cols=numerical_cols_admissions, drop_last_row=False)
    ooc_agreements = sanitize_data(ooc_agreements, numerical_cols=numerical_cols_admissions, drop_last_row=False)
    
    # suffix_care_admissions = '_ca'; suffix_ooc = '_ooc'
    suffix_care_admissions = C.MERGE_SUFFIXES['suffix_care_admissions']
    suffix_ooc = C.MERGE_SUFFIXES['suffix_ooc']
    sda_col_name = 'Service Delivery Area'
    temp_df = care_admissions.merge(right=ooc_agreements, on=sda_col_name,
                                suffixes=(suffix_care_admissions, suffix_ooc))
    
    return temp_df

def get_caller_data():

    reports_by_caller = pd.read_csv(data_dir.joinpath('child_protection_reports/protection_reports_by_caller.csv'))
    numerical_cols_caller = ['Protection Reports']
    reports_by_caller = sanitize_data(reports_by_caller, numerical_cols=numerical_cols_caller, drop_last_row=True)
    return reports_by_caller

def get_data()->dict:
    df_reports = get_reports_data()
    df_care = get_care_data()
    df_caller = get_caller_data()

    datasets = {'reports':df_reports,
                'care':df_care,
                'caller':df_caller}

    return datasets

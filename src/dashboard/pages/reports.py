from src import utils
from src import processing as p
from src.dashboard import viz
import pandas as pd
import streamlit as st


def sec_filter_pop():

    options = ['Total', 'Indigenous', 'Non-Indigenous']
    pop = st.sidebar.selectbox(label='Select population:',
                       options=options,
                       index=0)
    return pop


def sec_reports_flow(df_reports, df_care, SDA, population=None):

    viz.plot_reports_flow(df_reports=df_reports, df_care=df_care, SDA=SDA, pop=population)

def sec_sda_filter(df_reports:pd.DataFrame, sdc_col_name:str):

    def get_sda_col_names(df_reports, sda_col_name):
        sda_s = list(df_reports[sdc_col_name])
        return sda_s

    sda_s = get_sda_col_names(df_reports=df_reports, sda_col_name=sdc_col_name)

    select_sda = st.sidebar.selectbox(
        "select SDA:",
        options=sda_s,
        index=0
    )
    return select_sda

def sec_report_caller(df_caller:pd.DataFrame):

    view_as_percentage = st.checkbox(label="view as percentage", value=False)
    viz.plot_reports_by_caller(df_caller=df_caller, show_percentage=view_as_percentage)



def main(df_reports, df_care, df_caller, sda_col_name):

    select_sda = sec_sda_filter(df_reports=df_reports, sdc_col_name=sda_col_name)
    select_pop = sec_filter_pop()
    sec_reports_flow(df_reports=df_reports,df_care=df_care, SDA=select_sda, population=select_pop)
    sec_report_caller(df_caller=df_caller)


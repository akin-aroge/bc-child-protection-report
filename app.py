import streamlit as st
from src import utils
from src import processing as p
from src.dashboard import viz
from src.dashboard.pages import reports
import pandas as pd


st.set_page_config(page_title="BC-MCFD CHILD PROTECTION SERVICES REPORT", layout="wide")

proj_root_dir = utils.get_proj_root()
data_dir = proj_root_dir.joinpath('data/raw')

@st.cache_data
def get_data():
    return p.get_data()


def git_repo():
    st.caption(
        "Scource Code: [link](https://github.com/akin-aroge/bc-child-protection-report)"
    )

def data_sorce_link():
    st.caption(
        f""
    )

def sec_links_caption():
    cols = st.columns([0.1, 0.3, 0.6])
    with cols[0]:
        git_repo()
    with cols[1]:
        data_sorce_link()

def sec_synopsis():
    st.write(
        """
        Dashboard of Child Protection Reports for the 2022/2023 fiscal year.
"""
    )

def main():

    st.sidebar.title("Filters")
    st.title("BC MCFD CHILD PROTECTION SERVICES REPORT")
    sec_synopsis()
    sec_links_caption()

    datasets = get_data()
    df_reports = datasets['reports']
    df_care = datasets['care']
    df_caller = datasets['caller']
    sda_col_name = 'Service Delivery Area' 
    reports.main(df_reports=df_reports, df_care=df_care, df_caller=df_caller, sda_col_name=sda_col_name)


if __name__ == "__main__":
    main()

import streamlit as st
import src.processing as proc
import src.constants as C
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

TEMPLATE = "plotly_white"

def plot_reports_flow(df_reports:pd.DataFrame, df_care:pd.DataFrame, SDA=None, pop=None):

    sda_col_name = 'Service Delivery Area'

    if SDA is None:
        SDA='British Columbia'

    suffix_care_admissions = C.MERGE_SUFFIXES['suffix_care_admissions']
    suffix_ooc = C.MERGE_SUFFIXES['suffix_ooc']

    suffix_reports = C.MERGE_SUFFIXES['suffix_reports']
    suffix_reports_with_concern = C.MERGE_SUFFIXES['suffix_reports_with_concern']

    
    if pop is not None:
        col_for_reports =  pop
        if pop=='Total':
            col_for_reports = pop
            col_for_care = 'All'
        else:
            col_for_reports = 'Total '+ pop
            col_for_care = pop + ' (All)'
    else:
        col_for_reports = 'Total'
        col_for_care = 'All'

    total_with_concern = df_reports[df_reports[sda_col_name]==SDA][col_for_reports+suffix_reports_with_concern].values[0]
    total_reports = df_reports[df_reports[sda_col_name]==SDA][col_for_reports+suffix_reports].values[0]
    total_reports_no_concerns = total_reports - total_with_concern

    total_care_admissions = df_care[df_care[sda_col_name]==SDA][col_for_care+suffix_care_admissions].values[0]
    total_ooc = df_care[df_care[sda_col_name]==SDA][col_for_care+suffix_ooc].values[0]

    total_with_fam = total_with_concern - total_care_admissions
    total_with_fam_home = total_with_concern - total_care_admissions-total_ooc

    total_reports_no_concerns_pct = round(total_reports_no_concerns*100 / total_reports, 1)
    total_with_concern_pct = round(total_with_concern *100/ total_reports, 1)
    total_with_fam_pct = round(total_with_fam*100 / total_reports, 1)
    total_care_admissions_pct = round(total_care_admissions*100 / total_reports, 1)
    total_with_fam_home_pct = round(total_with_fam_home*100 / total_reports, 1)
    total_ooc_pct = round(total_ooc*100 / total_reports, 1)

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ["Reports", "safe", "with safety concerns",  "with family", "live at home", "with extendend family",
                    "in care"],
        customdata = ["Reports", "safe", "with safety concerns",  "with family", "live at home", "with extendend family",
                    "in care"],
        # hovertemplate = 'Node %{customdata} has total value %{value}<extra></extra>',
        color = "blue",
        ),
        link = dict(
        source = [0, 0, 2, 2, 3, 3], # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = [1, 2, 3, 6, 4, 5],
        value = [total_reports_no_concerns, 
                total_with_concern, 
                total_with_fam, 
                total_care_admissions, 
                total_with_fam_home,
                total_ooc],
        customdata = [total_reports_no_concerns_pct, 
                total_with_concern_pct, 
                total_with_fam_pct, 
                total_care_admissions_pct, 
                total_with_fam_home_pct,
                total_ooc_pct],
                     hovertemplate='%{customdata}% of all reports received<br />'
    ))])

    SDA_text = SDA; pop_seg = pop

    if SDA == 'British Columbia':
        SDA_text = "all SDAs"
    if pop=='Total':
        pop_seg = "Total"

    title_text = f"Child Protection Reports (SDA:{SDA_text}, Population Segment:{pop_seg})"

    fig.update_layout(title_text=title_text, font_size=20)
    # fig.show()
    st.plotly_chart(fig)
    

def plot_reports_by_caller(df_caller:pd.DataFrame, show_percentage=False):

    df = df_caller.copy()
    x_col_name = 'Type of Caller'; y_col_name = 'Protection Reports'
    if show_percentage:
        df['percentage'] = df[y_col_name]*100.0 / df[y_col_name].sum()
        y_col_name = 'percentage'

    df.sort_values(by=y_col_name, inplace=True, ascending=False)
    fig = px.bar(df, y=y_col_name, x=x_col_name, text_auto='.2',
                #  text=['{:.2}'.format(val) for val in df[y_col_name].values],
            title="Protection Reports by Caller (ALL SDAs)", color_discrete_sequence=['blue'],
            template=TEMPLATE)
    fig.update_layout(height=600)
    st.plotly_chart(fig)
    


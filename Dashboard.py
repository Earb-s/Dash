import streamlit as st
import pandas as pd
import base64
import numpy as np
import time
import plotly.express as px
import openpyxl






st.set_page_config(layout="wide")
st.title('AGS Dash Board')

st.markdown("""Internal Additive & Green Solution Group at Research and Innovation Center , KaengKhoi , Saraburi
""")

col1 = st.sidebar
col2, col3 = st.columns((1,1))

col1.header('Select to filter')

df = pd.read_excel (r'Workload2.xlsx', sheet_name='query')
df['Start Time_'] = pd.to_datetime(df['Start Time'])
df['End Time_'] = pd.to_datetime(df['End Time'])
df['total time_'] = (df['End Time']-df['Start Time'])
df['total time_'] = ((df['total time_'].dt.components['hours']*60)+(df['total time_'].dt.components['minutes']))/60
df = df.drop(['Start Time', 'End Time', 'total time'], 1)

df2 = df.groupby([df['Start Time_'].dt.year.rename('year'),df['Start Time_'].dt.month_name().rename('month'),df['Assignee']])['total time_'].sum().reset_index()


selected_year = col1.multiselect('Please choose Year', df2['year'].unique(),df2['year'].unique())
selected_month = col1.multiselect('Please choose Year', df2['month'].unique(),df2['month'].unique())
selected_person = col1.multiselect('Please choose persons', df2['Assignee'].unique(),df2['Assignee'].unique())

df_selected_all2 = df2[(df2.Assignee.isin(selected_person)) & (df2.year.isin(selected_year)) & (df2.month.isin(selected_month))]

col2.markdown('Working Hours of choosen person(s)')
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
# Inject CSS with Markdown
col2.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
col2.dataframe(df_selected_all2)

col3.markdown('Pie chart of selected persons and time')
Pie = px.pie(df_selected_all2, values='total time_', names='Assignee')
col3.plotly_chart(Pie, use_container_width=True)

df3 = df.groupby([df['Start Time_'].dt.year.rename('year'),df['Start Time_'].dt.month_name().rename('month'),df['Project Name'],df['Assignee']])['total time_'].sum().reset_index()

sort_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df3.index = pd.CategoricalIndex(df3['month'], categories = sort_order , ordered = True)
df3 = df3.sort_index().reindex()


df_selected_all3 = df3[(df3.year.isin(selected_year)) & (df3.month.isin(selected_month)) & (df3.Assignee.isin(selected_person))]
P_history = px.bar(df_selected_all3, x="month", y="total time_", color="Project Name", title="Project Concentration History")
#st.markdown('Please note that : this chart includes all persons')
st.plotly_chart(P_history, use_container_width=True)

df4 = df.groupby([df['Start Time_'].dt.year.rename('year'),df['Start Time_'].dt.month_name().rename('month'),df['Project Name'],df['Assignee']])['total time_'].sum().reset_index()

df_selected_all4 = df4[(df4.year.isin(selected_year)) & (df4.month.isin(selected_month)) & (df4.Assignee.isin(selected_person))]
Per_history = px.bar(df_selected_all4, x="Assignee", y="total time_", color="Project Name", title="Persons to Project Concentration     Please note that : this chart includes all persons")
st.plotly_chart(Per_history, use_container_width=True)



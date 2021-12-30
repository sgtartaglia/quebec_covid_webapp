from os import write
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta



st.write("""
# Quebec Covid Case & Hospitalization Tracker
* Data Source: "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/"
---

""")

# hospitalizations: https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_HospitalisationsSelonStatutVaccinalEtAge.csv"
# cases: "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_CasSelonStatutVaccinalEtAge.csv"

st.sidebar.header("User Input")
col1,col2 = st.columns([0.2,1])

select_df = st.sidebar.selectbox('Hospitalizations or Cases', ['Cases','Hospitalizations'])
age_choice = st.sidebar.selectbox('Hospitalizations or Cases', ['Over 50','Under 50', 'All ages'])
last_30_days = col1.button(label='Last 30 Days')
all_time = col2.button(label='All time')


def show_df(select_df):

    if select_df == 'Cases':
        df = pd.read_csv("https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_CasSelonStatutVaccinalEtAge.csv")
        df['Date'] = pd.to_datetime(df["Date"]).dt.date
        df['GrAge_Declaration'] = df['GrAge_Declaration'].replace({'0-9 ans': 'Under 50','10-19 ans': 'Under 50','20-29 ans': 'Under 50','30-39 ans': 'Under 50','40-49 ans': 'Under 50'})
        df['GrAge_Declaration'] = df['GrAge_Declaration'].replace({'50-59 ans': 'Over 50','60-69 ans': 'Over 50','70-79 ans': 'Over 50','80-89 ans': 'Over 50','90 ans et plus': 'Over 50'})
        print(df)
        df = df.rename({'GrAge_Declaration':'age'}, axis=1)
        df_pivot = pd.pivot_table(values='Nb_Nvx_Cas', columns=['Statut_Vaccinal'], index=['Date','age'],data=df, aggfunc=np.sum).reset_index().rename_axis(None,axis=1)
        df_output = df_pivot
        df_output['Total'] = df_output['Non-vacciné'] + df_output['Vacciné 1 dose'] + df_output['Vacciné 2 doses']
        df_output = df_output[df_output['age'] != 'Inconnu']

        

    else:
        df = pd.read_csv("https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_HospitalisationsSelonStatutVaccinalEtAge.csv")
        df['Date'] = pd.to_datetime(df["Date"]).dt.date
        df['GrAge_Admission'] = df['GrAge_Admission'].replace({'0-9 ans': 'Under 50','10-19 ans': 'Under 50','20-29 ans': 'Under 50','30-39 ans': 'Under 50','40-49 ans': 'Under 50'})
        df['GrAge_Admission'] = df['GrAge_Admission'].replace({'50-59 ans': 'Over 50','60-69 ans': 'Over 50','70-79 ans': 'Over 50','80-89 ans': 'Over 50','90 ans et plus': 'Over 50'})
        df = df.rename({'GrAge_Admission':'age'}, axis=1)
        df_pivot = pd.pivot_table(values='Nb_Nvelles_Hosp', columns=['Statut_Vaccinal'], index=['Date','age'],data=df, aggfunc=np.sum).reset_index().rename_axis(None,axis=1)
        df_output = df_pivot
        df_output['Total'] = df_output['Non-vacciné'] + df_output['Vacciné 1 dose'] + df_output['Vacciné 2 doses']
        df_output = df_output[df_output['age'] != 'Inconnu']

    return df_output

def select_age(age_choice):
    if last_30_days:
        df_graph = show_df(select_df)
        df_graph = df_graph[df_graph['age'] == age_choice]
        df_graph = df_graph[-30:]
        fig, ax = plt.subplots()
        ax.plot(df_graph['Date'],df_graph['Non-vacciné'], label='Non-Vaxxed')
        ax.plot(df_graph['Date'],df_graph['Vacciné 1 dose'], label='1 dose')
        ax.plot(df_graph['Date'],df_graph['Vacciné 2 doses'], label='2 dose')
        plt.xticks(rotation=90)
        plt.legend()
        plt.title(select_df + ' ' + age_choice)
        st.write(select_df +' for '+ age_choice +' last 5 days')
        st.write(str(df_graph.iloc[-5]['Date']) + ': ' + str(df_graph.iloc[-5]['Total']))
        st.write(str(df_graph.iloc[-4]['Date']) + ': ' + str(df_graph.iloc[-4]['Total']))
        st.write(str(df_graph.iloc[-3]['Date']) + ': ' + str(df_graph.iloc[-3]['Total']))
        st.write(str(df_graph.iloc[-2]['Date']) + ': ' + str(df_graph.iloc[-2]['Total']))
        st.write(str(df_graph.iloc[-1]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
        st.pyplot(fig)
        st.write(df_graph.tail())
    elif all_time:
        df_graph = show_df(select_df)
        df_graph = df_graph[df_graph['age'] == age_choice]
        fig, ax = plt.subplots()
        ax.plot(df_graph['Date'],df_graph['Non-vacciné'], label='Non-Vaxxed')
        ax.plot(df_graph['Date'],df_graph['Vacciné 1 dose'], label='1 dose')
        ax.plot(df_graph['Date'],df_graph['Vacciné 2 doses'], label='2 dose')
        plt.xticks(rotation=90)
        plt.legend()
        plt.title(select_df + ' ' + age_choice)
        st.write(select_df +' for '+ age_choice +' last 5 days')
        st.write(str(df_graph.iloc[-5]['Date']) + ': ' + str(df_graph.iloc[-5]['Total']))
        st.write(str(df_graph.iloc[-4]['Date']) + ': ' + str(df_graph.iloc[-4]['Total']))
        st.write(str(df_graph.iloc[-3]['Date']) + ': ' + str(df_graph.iloc[-3]['Total']))
        st.write(str(df_graph.iloc[-2]['Date']) + ': ' + str(df_graph.iloc[-2]['Total']))
        st.write(str(df_graph.iloc[-1]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
        st.pyplot(fig)
        st.write(df_graph.tail())
    else:
        df_graph = show_df(select_df)
        df_graph = df_graph[df_graph['age'] == age_choice]
        fig, ax = plt.subplots()
        ax.plot(df_graph['Date'],df_graph['Non-vacciné'], label='Non-Vaxxed')
        ax.plot(df_graph['Date'],df_graph['Vacciné 1 dose'], label='1 dose')
        ax.plot(df_graph['Date'],df_graph['Vacciné 2 doses'], label='2 dose')
        plt.xticks(rotation=90)
        plt.legend()
        plt.title(select_df + ' ' + age_choice)
        st.write(select_df +' for '+ age_choice +' last 5 days')
        st.write(str(df_graph.iloc[-5]['Date']) + ': ' + str(df_graph.iloc[-5]['Total']))
        st.write(str(df_graph.iloc[-4]['Date']) + ': ' + str(df_graph.iloc[-4]['Total']))
        st.write(str(df_graph.iloc[-3]['Date']) + ': ' + str(df_graph.iloc[-3]['Total']))
        st.write(str(df_graph.iloc[-2]['Date']) + ': ' + str(df_graph.iloc[-2]['Total']))
        st.write(str(df_graph.iloc[-1]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
        st.pyplot(fig)
        st.write(df_graph.tail())

if age_choice == 'Over 50':
    select_age(age_choice)

elif age_choice == 'Under 50':
    select_age(age_choice)
else:
    df_graph = show_df(select_df)
    df_graph = df_graph.groupby('Date').agg(np.sum).reset_index()
    fig, ax = plt.subplots()
    ax.plot(df_graph['Date'],df_graph['Non-vacciné'], label='Non-Vaxxed')
    ax.plot(df_graph['Date'],df_graph['Vacciné 1 dose'], label='1 dose')
    ax.plot(df_graph['Date'],df_graph['Vacciné 2 doses'], label='2 dose')
    plt.xticks(rotation=90)
    plt.legend()
    plt.title(select_df + ' ' + age_choice)
    st.write(select_df +' for '+ age_choice +' last 5 days')
    st.write(str(df_graph.iloc[-5]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
    st.write(str(df_graph.iloc[-4]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
    st.write(str(df_graph.iloc[-3]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
    st.write(str(df_graph.iloc[-2]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
    st.write(str(df_graph.iloc[-1]['Date']) + ': ' + str(df_graph.iloc[-1]['Total']))
    st.pyplot(fig)
    
    





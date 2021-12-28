import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date



st.write("""
# Quebec Covid Case & Hospitalization Tracker
* Data Source: "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_Vaccination_CatAge.csv"

""")
st.write(date.today())

# hospitalizations: https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_HospitalisationsSelonStatutVaccinalEtAge.csv"
# cases: "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_CasSelonStatutVaccinalEtAge.csv"

st.sidebar.header("User Input")

select_df = st.sidebar.selectbox('Hospitalizations or Cases', ['Cases','Hospitalizations'])
age_choice = st.sidebar.selectbox('Hospitalizations or Cases', ['Over 50','Under 50', 'All ages'])


def show_df(select_df):

    if select_df == 'Cases':
        df = pd.read_csv("https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_CasSelonStatutVaccinalEtAge.csv")
        df['Date'] = pd.to_datetime(df["Date"])
        df['GrAge_Declaration'] = df['GrAge_Declaration'].replace({'0-9 ans': 'Under 50','10-19 ans': 'Under 50','20-29 ans': 'Under 50','30-39 ans': 'Under 50','40-49 ans': 'Under 50'})
        df['GrAge_Declaration'] = df['GrAge_Declaration'].replace({'50-59 ans': 'Over 50','60-69 ans': 'Over 50','70-79 ans': 'Over 50','80-89 ans': 'Over 50','90 ans et plus': 'Over 50'})
        df = df.rename({'GrAge_Declaration':'age'}, axis=1)
        df_pivot = pd.pivot_table(values='Nb_Nvx_Cas', columns=['Statut_Vaccinal'], index=['Date','age'],data=df, aggfunc=np.sum)
        df_output = df_pivot.reset_index()
        df_output = df_output[df_output['age'] != 'Inconnu']

        

    else:
        df = pd.read_csv("https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_HospitalisationsSelonStatutVaccinalEtAge.csv")
        df['Date'] = pd.to_datetime(df["Date"])
        df['GrAge_Admission'] = df['GrAge_Admission'].replace({'0-9 ans': 'Under 50','10-19 ans': 'Under 50','20-29 ans': 'Under 50','30-39 ans': 'Under 50','40-49 ans': 'Under 50'})
        df['GrAge_Admission'] = df['GrAge_Admission'].replace({'50-59 ans': 'Over 50','60-69 ans': 'Over 50','70-79 ans': 'Over 50','80-89 ans': 'Over 50','90 ans et plus': 'Over 50'})
        df = df.rename({'GrAge_Admission':'age'}, axis=1)
        df_pivot = pd.pivot_table(values='Nb_Nvelles_Hosp', columns=['Statut_Vaccinal'], index=['Date','age'],data=df, aggfunc=np.sum)
        df_output = df_pivot.reset_index()
        df_output = df_output[df_output['age'] != 'Inconnu']

    return df_output


if age_choice == 'Over 50':
    df_graph = show_df(select_df)
    df_graph = df_graph[df_graph['age'] == 'Over 50']
    fig, ax = plt.subplots()
    ax.plot(df_graph['Date'],df_graph['Non-vacciné'], label='Non-Vaxxed')
    ax.plot(df_graph['Date'],df_graph['Vacciné 1 dose'], label='1 dose')
    ax.plot(df_graph['Date'],df_graph['Vacciné 2 doses'], label='2 dose')
    plt.xticks(rotation=90)
    plt.legend()
    st.pyplot(fig)

elif age_choice == 'Under 50':
    df_graph = show_df(select_df)
    df_graph = df_graph[df_graph['age'] == 'Under 50']
    fig, ax = plt.subplots()
    ax.plot(df_graph['Date'],df_graph['Non-vacciné'], label='Non-Vaxxed')
    ax.plot(df_graph['Date'],df_graph['Vacciné 1 dose'], label='1 dose')
    ax.plot(df_graph['Date'],df_graph['Vacciné 2 doses'], label='2 dose')
    plt.xticks(rotation=90)
    plt.legend()
    st.pyplot(fig)

else:
    df_graph = show_df(select_df)
    df_graph = df_graph.groupby('Date').agg(np.sum).reset_index()
    fig, ax = plt.subplots()
    ax.plot(df_graph['Date'],df_graph['Non-vacciné'], label='Non-Vaxxed')
    ax.plot(df_graph['Date'],df_graph['Vacciné 1 dose'], label='1 dose')
    ax.plot(df_graph['Date'],df_graph['Vacciné 2 doses'], label='2 dose')
    plt.xticks(rotation=90)
    plt.legend()
    st.pyplot(fig)


    
    





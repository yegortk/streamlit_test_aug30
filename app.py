import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd

url = 'https://raw.githubusercontent.com/globaldothealth/monkeypox/main/timeseries-country-confirmed.csv'

st.set_page_config(
    page_title="Monkeypox Dashboard",
    page_icon="🐒",
    layout="wide",
)

@st.experimental_memo
def get_data():
    data = pd.read_csv(url)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month'] = data['Date'].dt.month
    country_dynamics = data.pivot_table(index='Country', 
                               columns='Month', 
                               values='Cases', 
                               aggfunc='sum').fillna(0)
    return country_dynamics

data = get_data()

st.title("Monkeypox Dashboard")
default_ix = data.index.tolist().index('United States')
country_filter = st.selectbox("Select the Country", data.index, 
    index=default_ix)

placeholder = st.empty()
data = data.loc[country_filter]

with placeholder.container():
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="Total cases", value=round(data.sum()))
    kpi2.metric(label="Cases per month", value=int(data.mean()))
    
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Case dynamics")
        fig, ax = plt.subplots()
        ax.plot(data.index, data.values)
        plt.xlabel('Month (in 2022)')
        plt.ylabel('Total monkeypox confirmed cases')
        st.pyplot(fig)
        
    st.markdown("### Detailed Data View")
    st.dataframe(data)
    time.sleep(1)
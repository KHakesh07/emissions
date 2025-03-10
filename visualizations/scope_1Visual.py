import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer 


def fetch_data():
    conn = sqlite3.connect("data/emissions.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Scope1")
    data = cursor.fetchall()
    conn.close()
    return data

def display():
    st.title("Scope-1 Emissions Data")
    data = fetch_data()
    df = pd.DataFrame(data, columns=["Id","FuelType","Consumption (kWh)", "Emission (kg CO₂)"])
    dataframe = dataframe_explorer(df)
    st.dataframe(dataframe, use_container_width=True)
    
    st.write(" ")
    st.write(" ")
    st.write(" ")
     # Togle switch
    on = st.toggle(" Visualize the data using Pi chart ?")
    if on:
         fig = px.pie(df, names="FuelType", values="Emission (kg CO₂)", color="Consumption (kWh)",
                 title="Emission & Consumption Trend by Fuel Type", hole=0.3)
         st.plotly_chart(fig, use_container_width=True)
     # Pie Chart
    else:
         fig = px.line(df, x=["Emission (kg CO₂)", "Consumption (kWh)"], y="FuelType", 
                  markers=True, title="Emission & Consumption Trend by Fuel Type")
         st.plotly_chart(fig, use_container_width=True)
  

    des = st.selectbox("Select the Columns For Analysis:", ["Consumption (kWh)", "Emission (kg CO₂)"])
    st.subheader("Descriptive Analysis")

    totat= round(df[des].sum(), 3)
    avg = round(df[des].mean(), 3)
    max = round(df[des].max(), 3)
    min = round(df[des].min(), 3)
    no_of = df[des].count()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f'Total {des}', value=totat, border=True)
    with col2:
        st.metric(label=f'Average {des}', value=avg, border=True)
    with col3:
        st.metric(label=f'Highest Recorded {des}', value=max, border=True)

    col4, col5 = st.columns(2)
    with col4:
        st.metric(label=f'Lowest Recorded {des}', value=min, border=True)
    with col5:
        st.metric(label=f'Number of {des}\'s Recorded', value=no_of, border=True)


    cat = st.selectbox("Select the plot for visualize the data:", ["Pi Chart", "Scatter", "Bar Plot"])
    if cat == "Pi Chart":
          fig = px.pie(df, values=des, names='FuelType', title=f"{des} Breakdown", hole=0.3)
          st.plotly_chart(fig, use_container_width=True)
    elif cat == "Scatter":
            fig = px.scatter(df, x="FuelType", y=des, title=f"{des} Distribution", color='Emission (kg CO₂)', color_continuous_scale="Blues", template="plotly_dark", size_max=15)
            fig.update_traces(marker=dict(size=12, line=dict(width=1, color="black")))
            st.plotly_chart(fig, use_container_width=True)
        
    elif cat == "Bar Plot":
            fig = st.bar_chart(df, x="FuelType", y=des, color=des)

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


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
    st.table(df)
    st.subheader("Descriptive Analysis")
    des = st.selectbox("Select the Columns Header:", ["Consumption (kWh)", "Emission (kg CO₂)"])
    st.write(df[des].describe())

    cat = st.selectbox("Select the plot for visualize the data:", ["Scatter", "Bar Plot", "Line Graph"])
    if cat == "Scatter":
            cols = st.selectbox("Select Columns to display:", ["FuelType","Consumption (kWh)"])
            fig = px.scatter(df, x=df[cols], y="Emission (kg CO₂)", title="Emission Distribution", color='Emission (kg CO₂)', color_continuous_scale="Blues", template="plotly_dark", size_max=15)
            fig.update_traces(marker=dict(size=12, line=dict(width=1, color="black")), hovertemplate="<b>Quantity:</b> %{x} kg<br><b>CO₂ Emission:</b> %{y} kg")
            st.plotly_chart(fig, use_container_width=True)
        
    elif cat == "Bar Plot":
            fig = st.bar_chart(df, x="FuelType", y="Emission (kg CO₂)", color="Consumption (kWh)")
    elif cat == "Line Graph":
            fig = st.line_chart(df, x="Emission (kg CO₂)", y="Consumption (kWh)", color="Emission (kg CO₂)")

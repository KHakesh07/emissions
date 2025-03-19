import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from streamlit_extras.dataframe_explorer import dataframe_explorer


def visualize(category):
    conn = sqlite3.connect("data/emissions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, event, Weight, Quantity, Emission, Timestamp FROM Materials WHERE Category = ?", (category,))
    data = cursor.fetchall()
    conn.close()
   
    st.subheader("Stored Data")
    if data:
        df = pd.DataFrame(data, columns=["id","event", "Weight", "Quantity", "Emission","Timestamp"])
        df["Weight"] = df["Weight"].astype(float)
        df["Quantity"] = df["Quantity"].astype(float)
        df["Emission"] = df["Emission"].astype(float) # Convert Weight column to float
        st.table(df)


        fig = px.scatter(df, x="Timestamp", y="Emission", size="Quantity", color="Emission",
                             title="Total Emission by Events", color_continuous_scale="Blues")
        fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="black")))
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Descriptive Analysis")
        total_emission = round(df["Emission"].sum(), 3)
        avg_emission = round(df["Emission"].mean(), 3)
        max_emission = round(df["Emission"].max(), 3)
        min_emission = round(df["Emission"].min(), 3)
        day_with_highest_emission = df["Timestamp"].max()
        no_of_emissions = df["Emission"].count()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='Total Emission (kg CO₂)', value=total_emission)
        with col2:
            st.metric(label='Average Emission (kg CO₂)', value=avg_emission)
        with col3:
            st.metric(label='Highest Recorded Emission (kg CO₂)', value=max_emission)
        
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric(label='Lowest Recorded Emission (kg CO₂)', value=min_emission)
        with col5:
            st.metric(label='Number of Emissions Recorded', value=no_of_emissions)
        with col6:
            st.metric(label="The highest emission recorded day", value=day_with_highest_emission)
        
        st.subheader("Emissions Visualization")
        chart_type = st.selectbox("Select chart type:", ["Scatter", "Bar Plot"])
        
        if chart_type == "Scatter":
            fig = px.scatter(df, x="Weight", y="Emission", size="Quantity", color="Emission",
                             title="Weight vs CO₂ Emission", color_continuous_scale="Blues")
            fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="black")))
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Bar Plot":
            fig = px.bar(df, x="Quantity", y="Emission", text="Emission", color="Emission",
                         color_continuous_scale="Blues", title="Quantity vs CO₂ Emission")
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No records found.")


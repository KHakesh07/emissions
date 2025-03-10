import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_extras.dataframe_explorer import dataframe_explorer
import plotly.express as px

def electricity_visual():
    tab1, tab2 = st.tabs(["ElectricityEmissions", "HVAC Emissions"])

    with tab1:
        if "electricity_data" not in st.session_state:
            conn = sqlite3.connect('data/emissions.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Usage, Value, Emission FROM ElectricityEmissions")
            st.session_state.electricity_data = cursor.fetchall()
            conn.close()

        st.subheader("⚡ Electricity Emission Data")
        if st.session_state.electricity_data:
            df = pd.DataFrame(st.session_state.electricity_data, columns=["Usage", "Consumption (kWh)", "Emission (kg CO₂)"])
            dataframe = dataframe_explorer(df)
            st.dataframe(dataframe, use_container_width=True)

            total_emission = round(df["Emission (kg CO₂)"].sum(), 3)
            avg_emission = round(df["Emission (kg CO₂)"].mean(), 3)
            max_emission = round(df["Emission (kg CO₂)"].max(), 3)
            min_emission = round(df["Emission (kg CO₂)"].min(), 3)
            no_of_emissions = df["Emission (kg CO₂)"].count()

            # Display insights
            st.subheader("Descriptive analytics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label='Total Emission (kg CO₂)', value=total_emission, border=True)
            with col2:
                st.metric(label='Average Emission (kg CO₂)', value=avg_emission, border=True)
            with col3:
                st.metric(label='Highest Recorded Emission (kg CO₂)', value=max_emission, border=True)

            col4, col5 = st.columns(2)
            with col4:
                st.metric(label='Lowest Recorded Emission (kg CO₂)', value=min_emission, border=True)
            with col5:
                st.metric(label='Number of Emissions Recorded', value=no_of_emissions, border=True)


            d1, d2 = st.tabs(["Pi Chart", "Bar Plot"])
            with d1:
                fig = px.pie(df, names='Usage', values="Emission (kg CO₂)", color="Consumption (kWh)", title="Emissions Breakdown", hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
            with d2:
                fig = px.bar(df, x="Usage", y="Emission (kg CO₂)", text="Emission (kg CO₂)", color="Consumption (kWh)", color_continuous_scale="blues", labels={"Usage": "usage", "Emission (kg CO₂)": "CO₂ Emission (kg)"}, title="Emission Distribution")
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(fig, use_container_width=True)

            st.write("Breakdown Between Consumption and Emission")
            st.area_chart(df[["Consumption (kWh)", "Emission (kg CO₂)"]])

        else:
            st.write("No electricity emission records found.")

    with tab2:
        if "hvac_data" not in st.session_state:
            conn = sqlite3.connect('data/emissions.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Refrigerant, MassLeak, Emission FROM HVACEmissions")
            st.session_state.hvac_data = cursor.fetchall()
            conn.close()

        st.subheader("❄️ HVAC Emission Data")
        if st.session_state.hvac_data:
            df = pd.DataFrame(st.session_state.hvac_data, columns=["Refrigerant", "Mass Leak (kg)", "Emission (kg CO₂)"])
            dataframe = dataframe_explorer(df)
            st.dataframe(dataframe, use_container_width=True)

            total_emission = round(df["Emission (kg CO₂)"].sum(), 3)
            avg_emission = round(df["Emission (kg CO₂)"].mean(), 3)
            max_emission = round(df["Emission (kg CO₂)"].max(), 3)
            min_emission = round(df["Emission (kg CO₂)"].min(), 3)
            no_of_emissions = df["Emission (kg CO₂)"].count()

            # Display insights
            st.subheader("Descriptive analytics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label='Total Emission (kg CO₂)', value=total_emission, border=True)
            with col2:
                st.metric(label='Average Emission (kg CO₂)', value=avg_emission, border=True)
            with col3:
                st.metric(label='Highest Recorded Emission (kg CO₂)', value=max_emission, border=True)

            col4, col5 = st.columns(2)
            with col4:
                st.metric(label='Lowest Recorded Emission (kg CO₂)', value=min_emission, border=True)
            with col5:
                st.metric(label='Number of Emissions Recorded', value=no_of_emissions, border=True)

            st.write("Visaulizing the data using plots")
            d1, d2 = st.tabs(["Pi Chart", "Bar Plot"])
            with d1:
                fig = px.pie(df, names='Refrigerant', values="Emission (kg CO₂)", color="Mass Leak (kg)", title="Emissions Breakdown", hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
            with d2:
                fig = px.bar(df, x="Refrigerant", y="Emission (kg CO₂)", text="Emission (kg CO₂)", color="Mass Leak (kg)", color_continuous_scale="blues", title="Emission Distribution")
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="white", font=dict(size=14))
                st.plotly_chart(fig, use_container_width=True)

            st.write("Breakdown between Mass Leak & Emission by Refrigerant")
            fig = px.scatter_3d(df, x="Refrigerant", y="Emission (kg CO₂)", z="Mass Leak (kg)")
            fig.update_layout(width=700, height=500)
            st.plotly_chart(fig, use_container_width=True)


            
        else:
            st.write("No HVAC emission records found.")
import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

def electricity_visual(table):
    if table == "Electricity Emissions":
        if "electricity_data" not in st.session_state:
            conn = sqlite3.connect("emissions.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Usage, Value, Emission FROM ElectricityEmissions")
            st.session_state.electricity_data = cursor.fetchall()
            conn.close()

        st.subheader("⚡ Electricity Emission Data")
        if st.session_state.electricity_data:
            df = pd.DataFrame(st.session_state.electricity_data, columns=["Usage", "Consumption (kWh)", "Emission (kg CO₂)"])
            st.table(df)

            st.write(f"**Total Electricity Emissions:** {df['Emission (kg CO₂)'].sum():.2f} kg CO₂")
            st.write(f"**Average Emission per kWh:** {df['Emission (kg CO₂)'].mean():.2f} kg CO₂")
            st.write(f"**Maximum Emission Recorded:** {df['Emission (kg CO₂)'].max():.2f} kg CO₂")

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(df["Usage"], df["Emission (kg CO₂)"], color="green", edgecolor="black")
            ax.set_xlabel("Usage Type")
            ax.set_ylabel("CO₂ Emission (kg)")
            ax.set_title("Electricity Emissions by Usage")
            st.pyplot(fig)
        else:
            st.write("No electricity emission records found.")

    elif table == "HVAC Emissions":
        if "hvac_data" not in st.session_state:
            conn = sqlite3.connect("emissions.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Refrigerant, MassLeak, Emission FROM HVACEmissions")
            st.session_state.hvac_data = cursor.fetchall()
            conn.close()

        st.subheader("❄️ HVAC Emission Data")
        if st.session_state.hvac_data:
            df = pd.DataFrame(st.session_state.hvac_data, columns=["Refrigerant", "Mass Leak (kg)", "Emission (kg CO₂)"])
            st.table(df)

            st.write(f"**Total HVAC Emissions:** {df['Emission (kg CO₂)'].sum():.2f} kg CO₂")
            st.write(f"**Average Emission per Leak:** {df['Emission (kg CO₂)'].mean():.2f} kg CO₂")
            st.write(f"**Maximum Emission Recorded:** {df['Emission (kg CO₂)'].max():.2f} kg CO₂")

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(df["Refrigerant"], df["Emission (kg CO₂)"], color="blue", edgecolor="black")
            ax.set_xlabel("Refrigerant Type")
            ax.set_ylabel("CO₂ Emission (kg)")
            ax.set_title("HVAC Emissions by Refrigerant")
            st.pyplot(fig)
        else:
            st.write("No HVAC emission records found.")
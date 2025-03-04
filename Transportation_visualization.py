import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def transport_visual(table):
    if "transport_data" not in st.session_state:
        conn = sqlite3.connect("emissions.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT Mode, Vehicle, WeightOrDistance, Emission FROM {table}")
        st.session_state.transport_data = cursor.fetchall()
        conn.close()

    st.subheader("🚗 Transport Emission Data")
    if st.session_state.transport_data:
        df = pd.DataFrame(st.session_state.transport_data, columns=["Mode", "Vehicle", "Distance (km)", "Emission (kg CO₂)"])
        st.table(df)
        st.write(df.describe())

        st.write(f"**Total Transport Emissions:** {df['Emission (kg CO₂)'].sum():.2f} kg CO₂")
        st.write(f"**Average Emission per Trip:** {df['Emission (kg CO₂)'].mean():.2f} kg CO₂")
        st.write(f"**Maximum Emission Recorded:** {df['Emission (kg CO₂)'].max():.2f} kg CO₂")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df["Vehicle"], df["Emission (kg CO₂)"], color="orange", edgecolor="black")
        ax.set_xlabel("Vehicle Type")
        ax.set_ylabel("CO₂ Emission (kg)")
        ax.set_title("Transport Emissions by Vehicle Type")
        st.pyplot(fig)
    else:
        st.write("No transport emission records found.")

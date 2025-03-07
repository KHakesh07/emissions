import streamlit as st
import pandas as pd
import sqlite3

dict = {
    'Diesel': 0.2496,
    "Furnance Oil": 0.2496,
    "Kerosene": 0.2566,
    "Coal": 0.3230,
    "LPG": 0.2106,
    "Fuel Oil": 0.2491,
    "Electricity": 0.82,
    "Solar Energy": 0
}

def calculate(FuelType, Consumption):
    if FuelType in dict:
        return Consumption * dict[FuelType]
     
def insert_scope1_data(FuelType, Consumption, Emission):
    try:
        conn = sqlite3.connect("data/emissions.db")
        c = conn.cursor()
        c.execute(f"INSERT INTO Scope1 (FuelType, Consumption, Emission) VALUES (?, ?, ?)", 
                  (FuelType, Consumption, Emission))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()

def display_Scope1():
    st.title("Scope 1 EMissions Calculator")
    FuelType = st.selectbox("Select the Fuel Type:", dict.keys())
    Consumption = st.number_input(f"Enter the Consumption for {FuelType} (in kWh):", min_value=0.0, step=0.1, value=0.0)
    Emission = calculate(FuelType, Consumption)
    if st.button("Calculate Emission"):
        insert_scope1_data(FuelType, Consumption, Emission)
        st.success(f"Emission from {Consumption} kWh of {FuelType}: {Emission:.3f} kg CO₂")

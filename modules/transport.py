import streamlit as st
import sqlite3

# 🚗 Emission Factors (kg CO₂ per unit)
EMISSION_FACTORS = {
    "Road": {
        "3-Wheeler CNG": 0.10768,
        "2-Wheeler": 0.04911,
        "4W Petrol": 0.187421,
        "4W CNG": 0.068,
        "BUS": 0.015161
    },
}

# ⚡ Electric Consumption (kWh per km)
ELECTRIC_CONSUMPTION = {
    "Electric 2-Wheeler": 0.0319,  
    "Electric 4-Wheeler": 0.1277,
    "Local Train (Electricity)": 0.82  # Now under electric vehicles
}

# 🧮 Calculate Emission
def calculate_transport_emission(mode, vehicle, distance):
    if vehicle in EMISSION_FACTORS.get(mode, {}):
        return distance * EMISSION_FACTORS[mode][vehicle]  # kg CO₂ for fuel-based vehicles
    elif vehicle in ELECTRIC_CONSUMPTION:
        return distance * ELECTRIC_CONSUMPTION[vehicle] * 0.5  # Assuming 0.5 kg CO₂ per kWh for EVs
    return 0  # Default if no match found

# 📌 Insert Data into DB
def insert_transport_data(mode, vehicle, distance, emission):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute("INSERT INTO TransportEmissions (Mode, Vehicle, WeightOrDistance, Emission) VALUES (?, ?, ?, ?)", 
              (mode, vehicle, distance, emission))
    conn.commit()
    conn.close()

# 🚛 Show Transport Calculator
def show_transport_calculator():
    st.subheader("🚛 Transport Emission Calculator")

    mode = "Road"

    # Separate fuel-based and electric vehicles
    fuel_vehicles = list(EMISSION_FACTORS.get(mode, {}).keys())
    electric_vehicles = list(ELECTRIC_CONSUMPTION.keys()) if mode in ["Road", "Track"] else []  # 'Track' now includes electric trains

    vehicle_category = st.radio("Select Vehicle Type:", ["Fuel-Based", "Electric"], horizontal=True)

    if vehicle_category == "Fuel-Based":
        vehicle = st.selectbox("Select Vehicle:", fuel_vehicles)
    else:
        vehicle = st.selectbox("Select Electric Vehicle:", electric_vehicles)

    distance = st.number_input("Enter Distance Traveled (km):", min_value=0.1, step=0.1, value=1.0)

    if st.button("Calculate & Save", key="transport_calculate_save"):
        emission = calculate_transport_emission(mode, vehicle, distance)
        insert_transport_data(mode, vehicle, distance, emission)
        st.success(f"Emission for {distance} km using {vehicle}: {emission:.3f} kg CO₂")
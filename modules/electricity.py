import streamlit as st
import sqlite3

# ⚡ Electricity Consumption Emission Factors (kg CO₂ per kWh)
ELECTRICITY_EMISSION_FACTORS = {
    "Lighting and other electrical uses": 1.238,  
    "Cooling": 0.709
}

# ❄ HVAC Refrigerant Emission Factors
HVAC_REFRIGERANTS = {
    "R134a": {"EF (kg CO₂eq/kg)": 1300}  # Only EF remains fixed
}

# 🧮 Calculate Electricity Emissions
def calculate_electricity_emission(category, value):
    if category in ELECTRICITY_EMISSION_FACTORS:
        return value * ELECTRICITY_EMISSION_FACTORS[category]  # kg CO₂
    return 0  # Default if no match found

# 🧮 Calculate HVAC Emissions (with user-input mass leak)
def calculate_hvac_emission(refrigerant, mass_leak):
    if refrigerant in HVAC_REFRIGERANTS:
        ef = HVAC_REFRIGERANTS[refrigerant]["EF (kg CO₂eq/kg)"]
        return mass_leak * ef  # kg CO₂eq
    return 0

# 📌 Insert Electricity Data into DB
def insert_electricity_data(category, value, emission):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute("INSERT INTO ElectricityEmissions (Usage, Value, Emission) VALUES (?, ?, ?)", (category, value, emission))
    conn.commit()
    conn.close()

# 📌 Insert HVAC Data into DB
def insert_hvac_data(refrigerant, mass_leak, emission):
    conn = sqlite3.connect('data/emissions.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO HVACEmissions (Refrigerant, MassLeak, Emission) VALUES (?, ?, ?)", 
        (refrigerant, mass_leak, emission)
    )
    conn.commit()
    conn.close()

# ⚡ Show Electricity & HVAC Calculator
def show_electricity_hvac_calculator():
    st.subheader("⚡ Electricity & HVAC Emission Calculator")


    #tabs
    tab1, tab2 = st.tabs(["Electricity", "HVAC"])
    with tab1:
        # 🔋 Electricity Usage Section
        st.write("### 🔋 Electricity Consumption")
        category = st.selectbox("Select Energy Use Category", list(ELECTRICITY_EMISSION_FACTORS.keys()))
        value = st.number_input(f"Enter Consumption for {category} (kWh):", min_value=0.0, step=0.1, value=0.0)

        # Assign a unique key for the electricity calculation button.
        if st.button("Calculate Electricity Emission", key="electricity_calc_button"):
            emission = calculate_electricity_emission(category, value)
            insert_electricity_data(category, value, emission)
            st.success(f"Emission from {value} kWh in {category}: {emission:.3f} kg CO₂")

    # with tab2
    with tab2:
        # ❄ HVAC Leakage Section
        st.write("### ❄ HVAC Refrigerant Leakage")
        refrigerant = st.selectbox("Select Refrigerant", list(HVAC_REFRIGERANTS.keys()))
        mass_leak = st.number_input(f"Enter Mass Leak for {refrigerant} (kg):", min_value=0.0, step=0.01, value=0.0)

        # Assign a unique key for the HVAC calculation button.
        if st.button("Calculate HVAC Emission", key="hvac_calc_button"):
            emission = calculate_hvac_emission(refrigerant, mass_leak)
            insert_hvac_data(refrigerant, mass_leak, emission)
            st.success(f"Emission from {mass_leak} kg leakage of {refrigerant}: {emission:.3f} kg CO₂eq")
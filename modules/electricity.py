import streamlit as st
import sqlite3

# ⚡ Electricity Consumption Emission Factors (kg CO₂ per kWh)
ELECTRICITY_EMISSION_FACTORS = {
    "Lighting and other electrical uses": 1.238,  
    "Cooling": 0.709
}

# ❄ HVAC Refrigerant Emission Factors
HVAC_REFRIGERANTS = {
    "R134a": {"EF (kg CO₂eq/kg)": 1300},  # Only EF remains fixed
    'R-32': {"EF (kg CO₂eq/kg)": 677},
    'R-410A': {"EF (kg CO₂eq/kg)": 2088},
    'R-290': {"EF (kg CO₂eq/kg)": 3},
    'R-404A': {"EF (kg CO₂eq/kg)": 3922},
    'R-407C': {"EF (kg CO₂eq/kg)": 1774},   
    'R-407A': {"EF (kg CO₂eq/kg)": 2107},
    'R-407F': {"EF (kg CO₂eq/kg)": 1824},
    'R-1234yf': {"EF (kg CO₂eq/kg)": 4},
    'R-1234ze(E)': {"EF (kg CO₂eq/kg)": 6},
    'R-600a': {"EF (kg CO₂eq/kg)": 3},
    'R-744': {"EF (kg CO₂eq/kg)": 1},
    'R-123': {"EF (kg CO₂eq/kg)": 77},
    'R-245fa': {"EF (kg CO₂eq/kg)": 1030},
    'R-600': {"EF (kg CO₂eq/kg)": 3},
    'R-32/R-125': {"EF (kg CO₂eq/kg)": 677},
    'R-507A': {"EF (kg CO₂eq/kg)": 3985},'R-508B': {"EF (kg CO₂eq/kg)": 13900},
    'R-23': {"EF (kg CO₂eq/kg)": 14800},'R-134': {"EF (kg CO₂eq/kg)": 1300},
    'R-717': {"EF (kg CO₂eq/kg)": 1}
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

    # Tabs for Electricity and HVAC
    tab1, tab2 = st.tabs(["Electricity", "HVAC"])

    with tab1:
        # 🔋 Electricity Consumption Section
        st.write("### 🔋 Electricity Consumption")
        category = st.selectbox("Select Energy Use Category", list(ELECTRICITY_EMISSION_FACTORS.keys()))
        value = st.number_input(f"Enter Consumption for {category} (kWh):", min_value=0.0, step=0.1, value=0.0)

        if st.button("Calculate Electricity Emission", key="electricity_calc_button"):
            emission = calculate_electricity_emission(category, value)
            insert_electricity_data(category, value, emission)
            st.success(f"Emission from {value} kWh in {category}: {emission:.3f} kg CO₂")

    with tab2:
        # ❄ HVAC Refrigerant Leakage Section
        st.write("### ❄ HVAC Refrigerant Leakage")
        refrigerant = st.selectbox("Select Refrigerant", list(HVAC_REFRIGERANTS.keys()))
        mass_leak = st.number_input(f"Enter Mass Leak for {refrigerant} (kg):", min_value=0.0, step=0.01, value=0.0)

        if st.button("Calculate HVAC Emission", key="hvac_calc_button"):
            emission = calculate_hvac_emission(refrigerant, mass_leak)
            insert_hvac_data(refrigerant, mass_leak, emission)
            st.success(f"Emission from {mass_leak} kg leakage of {refrigerant}: {emission:.3f} kg CO₂eq")

            # Suggest Greener Alternatives
            st.write("### 🌱 Greener Alternatives")
            current_ef = HVAC_REFRIGERANTS[refrigerant]["EF (kg CO₂eq/kg)"]
            greener_options = []

            for alt_refrigerant, data in HVAC_REFRIGERANTS.items():
                alt_ef = data["EF (kg CO₂eq/kg)"]
                if alt_ef < current_ef:
                    reduction = ((current_ef - alt_ef) / current_ef) * 100
                    greener_options.append((alt_refrigerant, alt_ef, reduction))

            if greener_options:
                greener_options = sorted(greener_options, key=lambda x: x[1])  # Sort by EF (ascending)
                for alt_refrigerant, alt_ef, reduction in greener_options:
                    st.write(
                        f"- **{alt_refrigerant}**: EF = {alt_ef} kg CO₂eq/kg, "
                        f"**Reduction** = {reduction:.2f}%"
                    )
            else:
                st.info("No greener alternatives available for the selected refrigerant.")

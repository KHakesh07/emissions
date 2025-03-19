import streamlit as st
import sqlite3
import json

# Emission factors dictionary
emission_factors = {
    'Diesel': 0.2496,
    "Coal": 0.3230,
    "Petroleum Gas (LPG)": 0.2106,
    "Electricity": 0.82,
}

def calculate_emission(fuel_type, consumption):
    """Calculate emission based on fuel type and consumption."""
    return consumption * emission_factors.get(fuel_type, 0)

def insert_scope1_data(event, fuels, consumptions, emissions, total_emission):
    """Insert multiple fuel entries into the database."""
    try:
        conn = sqlite3.connect("data/emissions.db")
        c = conn.cursor()
        
        # Convert lists to JSON strings
        fuels_json = json.dumps(fuels)
        consumptions_json = json.dumps(consumptions)
        emissions_json = json.dumps(emissions)

        c.execute("""
            INSERT INTO Scope1 (event, fuels, consumptions, emissions, total_emission)
            VALUES (?, ?, ?, ?, ?)""",
            (event, fuels_json, consumptions_json, emissions_json, total_emission)
        )

        conn.commit()
        st.success("Emission data saved successfully!")
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

def display_scope1():
    st.title("Scope 1 Emissions Calculator")
    st.write("Scope 1 emissions refer to direct greenhouse gas (GHG) emissions from sources that are owned or controlled by an organization.")

    # Event input field
    event = st.text_input("Event Name", placeholder="Enter event name")

    # Initialize session state variables
    if "fuel_entries" not in st.session_state:
        st.session_state.fuel_entries = [{"id": 0, "fuel_type": "Diesel", "consumption": 0.0}]

    total_emission = 0  # Reset total emissions each time
    fuels, consumptions, emissions = [], [], []

    # Display fuel entries using columns
    for entry in st.session_state.fuel_entries:
        index = entry["id"]
        cols = st.columns([3, 3, 2])  # Set column widths

        with cols[0]:  # Fuel Type Selection
            fuel_type = st.selectbox(f"Fuel Type {index + 1}:", emission_factors.keys(),
                                     key=f"fuel_{index}", index=list(emission_factors.keys()).index(entry["fuel_type"]))

        with cols[1]:  # Consumption Input
            consumption = st.number_input(f"Consumption {index + 1} (kWh):",
                                          min_value=0.0, step=0.1, value=entry["consumption"],
                                          key=f"consumption_{index}")

        with cols[2]:  # Remove Entry Button
            if st.button("Remove", key=f"remove_{index}"):
                st.session_state.fuel_entries = [e for e in st.session_state.fuel_entries if e["id"] != index]
                st.rerun()

        emission = calculate_emission(fuel_type, consumption)
        total_emission += emission

        # Store values for database insertion
        fuels.append(fuel_type)
        consumptions.append(consumption)
        emissions.append(emission)

    # Display total emissions
    st.subheader(f"Total Emission: {total_emission:.3f} kg CO₂")

    # Save all fuel data
    if st.button("Save Emission Data"):
        if not event:
            st.error("Please enter an event name before saving!")
        else:
            insert_scope1_data(event, fuels, consumptions, emissions, total_emission)

    # Add another fuel entry
    if st.button("Add Another Fuel"):
        new_id = max([e["id"] for e in st.session_state.fuel_entries], default=-1) + 1
        st.session_state.fuel_entries.append({"id": new_id, "fuel_type": "Diesel", "consumption": 0.0})
        st.rerun()

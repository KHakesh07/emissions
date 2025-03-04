import streamlit as st
import sqlite3

# 🍲 Food Emission Factors (kg CO₂ per kg)
FOOD_EMISSION_FACTORS = {
    "Beef": 27.0,
    "Chicken": 6.9,
    "Rice": 2.7,
    "Vegetables": 2.0
}

# 🧮 Calculate Food Emission
def calculate_food_emission(food_item, quantity):
    if food_item in FOOD_EMISSION_FACTORS:
        return quantity * FOOD_EMISSION_FACTORS[food_item]
    return 0

# 📌 Insert Food Data into DB
def insert_food_data(food_item, quantity, emission):
    try:
        conn = sqlite3.connect("emissions.db")
        c = conn.cursor()
        c.execute("INSERT INTO FoodEmissions (FoodItem, Quantity, Emission) VALUES (?, ?, ?)", 
                  (food_item, quantity, emission))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()

# 🥗 Show Food Calculator
def show_food_calculator():
    st.subheader("🥗 Food Emission Calculator")

    food_item = st.selectbox("Select Food Item", list(FOOD_EMISSION_FACTORS.keys()))
    quantity = st.number_input("Enter Quantity (kg):", min_value=0.1, step=0.1, value=1.0)

    if st.button("Calculate & Save"):
        emission = calculate_food_emission(food_item, quantity)
        insert_food_data(food_item, quantity, emission)
        st.success(f"Emission for {quantity} kg of {food_item}: {emission:.3f} kg CO₂")

    if st.button("Back to Main Menu"):
        st.session_state.page = "main"
        st.rerun()